package com.lys.finova_system.controller;

import com.lys.finova_system.domain.Code;
import com.lys.finova_system.domain.ResultJSON;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloController {

    @GetMapping
    public String hello() {
        return "Hello";
    }

    @GetMapping("/1")
    public ResultJSON testCode1() {
        return new ResultJSON(Code.OK, "1");
    }

    @GetMapping("/2")
    public ResultJSON testCode2() {
        return new ResultJSON(Code.OK, "2", "好的");
    }

    @GetMapping("/3")
    public ResultJSON testCode3() {
        return new ResultJSON(Code.OK, "3");
    }
}
