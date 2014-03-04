/*
 * =====================================================================================
 *
 *       Filename:  EfficiencyTree.cc
 *
 *    Description:  Produce a tree for making efficiencies
 *                  Compares a reco object to an L1 object to a UCTObject.
 *
 *         Author:  Evan Friis, evan.friis@cern.ch
 *        Company:  UW Madison
 *
 * =====================================================================================
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "L1Trigger/UCT2015/interface/ExpressionNtuple.h"
#include "L1Trigger/UCT2015/interface/L1RecoMatch.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

typedef std::vector<edm::InputTag> VInputTag;
typedef std::vector<unsigned int> PackedUIntCollection;

class EfficiencyTree : public edm::EDAnalyzer {
  public:
    EfficiencyTree(const edm::ParameterSet& pset);
    virtual ~EfficiencyTree(){}
    void analyze(const edm::Event& evt, const edm::EventSetup& es);
  private:
    uct::ExpressionNtuple<L1RecoMatch> ntuple_;
    VInputTag recoSrc_;
    VInputTag l1Src_;
    VInputTag l1GSrc_;
    edm::InputTag l1GPUSrc_;
    edm::InputTag pvSrc_;
    double maxDR_;
    bool useVertex_;
};

EfficiencyTree::EfficiencyTree(const edm::ParameterSet& pset):
  ntuple_(pset.getParameterSet("ntuple")) {
    // Initialize the ntuple builder
    edm::Service<TFileService> fs;
    ntuple_.initialize(*fs);
    recoSrc_ = pset.getParameter<VInputTag>("recoSrc");
    pvSrc_ = pset.exists("pvSrc") ? pset.getParameter<edm::InputTag>("pvSrc") : edm::InputTag("offlinePrimaryVertices");
    l1Src_ = pset.getParameter<VInputTag>("l1Src");
    l1GSrc_ = pset.getParameter<VInputTag>("l1GSrc");
    l1GPUSrc_ = pset.getParameter<edm::InputTag>("l1GPUSrc");
    maxDR_ = pset.getParameter<double>("maxDR");
    useVertex_ = pset.exists("useVertex") ? pset.getParameter<bool>("useVertex") : true;
}

namespace {

// Turn a set of InputTags into a colleciton of candidate pointers.
std::vector<const reco::Candidate*> getCollections(
    const edm::Event& evt, const VInputTag& collections) {
  std::vector<const reco::Candidate*> output;
  // Loop over collections
  for (size_t i = 0; i < collections.size(); ++i) {
    edm::Handle<edm::View<reco::Candidate> > handle;
    evt.getByLabel(collections[i], handle);
    // Loop over objects in current collection
    for (size_t j = 0; j < handle->size(); ++j) {
      const reco::Candidate& object = handle->at(j);
      output.push_back(&object);
    }
  }
  return output;
}

// Find the reco::Candidate in the [l1Collection] closes in DeltaR to
// [recoObject].  Only objects within [maxDR] are considered.  If no match
// is found, NULL is returned.
const reco::Candidate* findBestMatch(const reco::Candidate* recoObject,
    std::vector<const reco::Candidate*>& l1Collection, double maxDR) {
  const reco::Candidate* output = NULL;
  double bestDeltaR = -1;
  for (size_t i = 0; i < l1Collection.size(); ++i) {
    double deltaR = reco::deltaR(*recoObject, *l1Collection[i]);
    if (deltaR < maxDR) {
      if (!output || deltaR < bestDeltaR) {
        output = l1Collection[i];
        bestDeltaR = deltaR;
      }
    }
  }
  return output;
}

}

void EfficiencyTree::analyze(const edm::Event& evt, const edm::EventSetup& es) {
  // Get the RECO and regular L1 corrections
  std::vector<const reco::Candidate*> recoObjects = getCollections(
      evt, recoSrc_);
  std::vector<const reco::Candidate*> l1Objects = getCollections(
      evt, l1Src_);
  std::vector<const reco::Candidate*> l1GObjects = getCollections(
      evt, l1GSrc_);

  // Get PV collection
  edm::Handle<reco::VertexCollection> vertices;
  if(useVertex_)
    evt.getByLabel(pvSrc_, vertices);

  // Now match reco objects to L1 objects
  std::vector<L1RecoMatch> matches;
  for (size_t i = 0; i < recoObjects.size(); ++i) {
    const reco::Candidate* recoObject = recoObjects[i];
    const reco::Candidate* bestL1 = findBestMatch(recoObject, l1Objects, maxDR_);
    const reco::Candidate* bestL1G = findBestMatch(recoObject, l1GObjects, maxDR_);
    int vertices_i = 1;
    if(useVertex_) vertices_i = vertices->size();
    L1RecoMatch theMatch(recoObject, bestL1, bestL1G, evt.id(),
						 matches.size(), recoObjects.size(), vertices_i);
    matches.push_back(theMatch);
  }

  // Now fill our TTree for each of the reco matches
  // NB each entry in the tree is a RECO object, not an event!
  for (size_t i = 0; i < matches.size(); ++i) {
    ntuple_.fill(matches[i]);
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(EfficiencyTree);
