package com.lys.finova_system.service;

import com.lys.finova_system.domain.ResultJSON;
import org.springframework.web.multipart.MultipartFile;

public interface LoadService {
    void init();

    String getPath(Integer num);

    ResultJSON handleUploadFile(Integer uid, MultipartFile file, Integer fileType);

    ResultJSON handleUploadFolder(Integer uid, MultipartFile[] files, Integer fileType);

}
