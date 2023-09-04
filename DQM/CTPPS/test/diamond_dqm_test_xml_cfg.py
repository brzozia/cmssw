import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('RECODQM', Run3)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.verbosity = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# minimum of logs
process.MessageLogger = cms.Service("MessageLogger",
    cerr = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING')
    )
)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# load DQM framework
process.load("DQM.Integration.config.environment_cfi")
process.dqmEnv.subSystemFolder = "CTPPS"
process.dqmEnv.eventInfoFolder = "EventInfo"
process.dqmSaver.path = ""
process.dqmSaver.tag = "CTPPS"

# raw data source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    # '/store/data/Run2018D/ZeroBias/AOD/12Nov2019_UL2018_rsb-v1/280000/FE61A0D8-CEDC-2142-81AA-06301F452792.root',
    '/store/data/Run2023D/ZeroBias/RAW/v1/000/370/749/00000/00e73a77-d415-499d-991e-6efd707f12e6.root'
    ),
)


from Configuration.AlCa.GlobalTag import GlobalTag
from Configuration.AlCa.autoCond import autoCond
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_hlt_relval', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, '120X_dataRun2_v2', '')
process.GlobalTag = GlobalTag(process.GlobalTag, autoCond['run3_data_prompt'], '')

process.GlobalTag.toGet = cms.VPSet(
        cms.PSet(record = cms.string("TotemReadoutRcd"),
                 tag = cms.string("PPSDAQMapping_TrackingStrip_test_v1"),
                 connect = cms.string("frontier://FrontierPrep/CMS_CONDITIONS"),
                 label = cms.untracked.string("TrackingStrip")
                 ),
        cms.PSet(record = cms.string("TotemReadoutRcd"),
                 tag = cms.string("PPSDAQMapping_TimingDiamond_test_v1"),
                 connect = cms.string("frontier://FrontierPrep/CMS_CONDITIONS"),
                 label = cms.untracked.string("TimingDiamond")
                 ),
        cms.PSet(record = cms.string("TotemReadoutRcd"),
                 tag = cms.string("PPSDAQMapping_TotemTiming_test_v1"),
                 connect = cms.string("frontier://FrontierPrep/CMS_CONDITIONS"),
                 label = cms.untracked.string("TotemTiming")
                 ),
        cms.PSet(record = cms.string("TotemReadoutRcd"),
                 tag = cms.string("PPSDAQMapping_TotemT2_test_v1"),
                 connect = cms.string("frontier://FrontierPrep/CMS_CONDITIONS"),
                 label = cms.untracked.string("TotemT2")
                 ),
        cms.PSet(record = cms.string("TotemAnalysisMaskRcd"),
                 tag = cms.string("PPSAnalysisMask_test_v1"),
                 connect = cms.string("frontier://FrontierPrep/CMS_CONDITIONS"),
                 )
        )

# raw-to-digi conversion
process.load("EventFilter.CTPPSRawToDigi.ctppsRawToDigi_xml_cff")

# prefer mappings from XML files
process.es_prefer_totemTimingMapping = cms.ESPrefer("TotemDAQMappingESSourceXML", "totemDAQMappingESSourceXML_TotemTiming", TotemReadoutRcd=cms.vstring("TotemDAQMapping/TotemTiming"))
process.es_prefer_totemDiamondMapping = cms.ESPrefer("TotemDAQMappingESSourceXML", "totemDAQMappingESSourceXML_TimingDiamond", TotemReadoutRcd=cms.vstring("TotemDAQMapping/TimingDiamond"))
process.es_prefer_totemT2Mapping = cms.ESPrefer("TotemDAQMappingESSourceXML", "totemDAQMappingESSourceXML_TotemT2", TotemReadoutRcd=cms.vstring("TotemDAQMapping/TotemT2"))
process.es_prefer_TrackingStripMapping = cms.ESPrefer("TotemDAQMappingESSourceXML", "totemDAQMappingESSourceXML_TrackingStrip", TotemReadoutRcd=cms.vstring("TotemDAQMapping/TrackingStrip"))

# local RP reconstruction chain with standard settings
process.load("RecoPPS.Configuration.recoCTPPS_cff")
process.load('Geometry.VeryForwardGeometry.geometryRPFromDD_2021_cfi')
# CTPPS DQM modules
process.load("DQM.CTPPS.ctppsDQM_cff")
process.ctppsDiamondDQMSource.excludeMultipleHits = cms.bool(True)
process.ctppsDiamondDQMSource.plotOnline = cms.untracked.bool(True)
process.ctppsDiamondDQMSource.plotOffline = cms.untracked.bool(False)
process.path = cms.Path(
    process.ctppsRawToDigi*
    process.recoCTPPS*
    process.ctppsDQMOnlineSource*
    process.ctppsDQMOnlineHarvest
)

process.end_path = cms.EndPath(
    process.dqmEnv +
    process.dqmSaver
)

process.schedule = cms.Schedule(
    process.path,
    process.end_path
)
