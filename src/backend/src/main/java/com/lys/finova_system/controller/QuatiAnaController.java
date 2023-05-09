package com.lys.finova_system.controller;

import com.lys.finova_system.domain.ResultJSON;
import com.lys.finova_system.service.QuatiAnaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.HashMap;

@RestController
@RequestMapping("/quatiAnalyses")
public class QuatiAnaController {
    @Autowired
    private QuatiAnaService quatiAnaService;

    @PostMapping("/present")
    public ResultJSON present(@RequestParam Integer alg, @RequestParam Integer stock) throws IOException {
        return quatiAnaService.handlePresent(alg, stock);
    }

    @PostMapping("/predict")
    public ResultJSON predict(String filePath, Integer alg) {
        // @RequestBody HashMap<String, Object> requestMap
        return null;
    }

}
