package com.lys.finova_system.dao;

import com.lys.finova_system.domain.UploadFile;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface UploadFileDao {

    @Insert("insert into uploadfile (file_name, type, file_num, file_path, uid) values(#{fileName}, #{type}, #{fileNum}, #{filePath}, #{uid})")
    @Options(useGeneratedKeys = true, keyProperty = "fid", keyColumn = "fid")

    Integer insert(UploadFile uploadFile);

    @Select("select * from uploadfile where fid = #{fid}")
    @Results(id = "uploadMap", value = {
            @Result(id = true, column = "fid", property = "fid"),
            @Result(column = "file_name", property = "fileName"),
            @Result(column = "type", property = "type"),
            @Result(column = "file_num", property = "fileNum"),
            @Result(column = "file_path", property = "filePath"),
            @Result(column = "uid", property = "uid")
    })
    UploadFile queryByFid(Integer fid);
}
