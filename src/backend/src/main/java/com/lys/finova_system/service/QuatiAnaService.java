package com.lys.finova_system.service;

import com.lys.finova_system.domain.ResultJSON;

import java.io.IOException;

public interface QuatiAnaService {
    void test();

    ResultJSON handlePresent(Integer alg, Integer stock) throws IOException;

    ResultJSON handlePredict(String filePath, Integer alg);



}
