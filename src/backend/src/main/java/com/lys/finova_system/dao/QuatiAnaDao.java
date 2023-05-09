package com.lys.finova_system.dao;

import com.lys.finova_system.domain.AnalyzeChart;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

@Mapper
@Repository
public interface QuatiAnaDao {
    @Select("select * from analyzechart where analyze_name = #{anaName}")
    @Results(id = "acMap", value = {
            @Result(id = true, column = "aid", property = "aid"),
            @Result(column = "analyze_name", property = "analyzeName"),
            @Result(column = "state", property = "state"),
            @Result(column = "path_prefix", property = "pathPrefix"),
            @Result(column = "alg_num", property = "algNum"),
            @Result(column = "stock_num", property = "stockNum")
    })
    AnalyzeChart queryByAnalyzeName(StringBuilder anaName);

    @Select("select * from analyzechart where alg_num = #{algNum} and stock_num = #{stockNum}")
    @ResultMap("acMap")
    AnalyzeChart queryByAlgAndStock(Integer algNum, Integer stockNum);

    @Insert("insert into analyzechart(aid, analyze_name, state, path_prefix, alg_num, stock_num) values(null, #{analyzeName}, #{state}, #{pathPrefix}, #{algNum}, #{stockNum})")
    @ResultMap("acMap")
    Integer insertAnalyzeChart(AnalyzeChart analyzeChart);

    @Update("update analyzechart set state = #{state}, path_prefix = #{pathPrefix}, where aid = #{aid}")
    @ResultMap("acMap")
    Integer updateStateAndOutputPath(AnalyzeChart analyzeChart);

}
