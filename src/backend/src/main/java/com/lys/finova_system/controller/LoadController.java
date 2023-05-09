package com.lys.finova_system.controller;

import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.service.LoadService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.support.StandardMultipartHttpServletRequest;

import javax.annotation.Resource;
import javax.servlet.ServletRequest;
import java.io.File;

@RestController
@RequestMapping("/loads")
public class LoadController {
    @Autowired
    private LoadService loadService;

    @PostMapping("/upload/file")
    public ResultJSON uploadFile(@RequestParam MultipartFile file, @RequestParam Integer uid, @RequestParam Integer fileType) {
        return loadService.handleUploadFile(uid, file, fileType);
    }

    @PostMapping("/upload/folder")
    public ResultJSON uploadFolder(@RequestParam MultipartFile[] folder, @RequestParam Integer uid, @RequestParam Integer folderType) {
        return loadService.handleUploadFolder(uid, folder, folderType);
    }


    @GetMapping("/download/{fileName}")
    public Resource getFile(@PathVariable("fileName") String filename) {

        return null;
    }
}
