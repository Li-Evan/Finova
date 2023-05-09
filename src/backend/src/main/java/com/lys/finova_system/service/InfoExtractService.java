package com.lys.finova_system.service;

import com.lys.finova_system.domain.ResultJSON;

public interface InfoExtractService {

    ResultJSON executeInquiryLetter(Integer fid, Integer algType);

    ResultJSON executeAnnualReport(Integer incomeFid, Integer cashflowFid, Integer assetsFid, Integer algType);
}
