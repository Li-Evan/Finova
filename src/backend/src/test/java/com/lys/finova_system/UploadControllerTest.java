package com.lys.finova_system;

import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import java.io.File;

@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class UploadControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void uploadFolderTest() throws Exception {
//        System.out.println("测试类");
        File file = new File("E:\\System\\Desktop\\finova_test\\123");
        MockMultipartFile multipartFile = new MockMultipartFile("file", "", "multipart/form-data", FileUtils.readFileToByteArray(file));
        Integer param1 = 1;
        Integer param2 = 1;

        mockMvc.perform(MockMvcRequestBuilders.multipart("/loads/upload/folder")
                        .file(multipartFile)
                        .param("uid", param1.toString())
                        .param("folderType", param2.toString()))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.content().string("File uploaded successfully!"));
    }
}
