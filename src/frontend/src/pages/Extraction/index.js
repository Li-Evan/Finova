import style from "./index.module.css";
import {makeStyle} from "../../utils/CSSUtils";
import {useEffect, useRef, useState} from "react";
import {http} from "../../utils";
import {ip} from "../../constIp";
import {getToken} from "../../utils";
import {LoadingOutlined} from "@ant-design/icons";
import * as echarts from 'echarts';
import {message} from "antd";
import {Histogram} from "../Histogram";
import {List, Typography, Tooltip} from 'antd'


const s = makeStyle(style)

function SideBar(props) {
    function clickSideBar(option) {
        props.clickSideBarItem(option)
    }

    return (<div className={s("sidebar-box")}>
        <div className={s("sidebar-content")} onClick={() => {
            clickSideBar("Inquiry")
        }} style={{
            backgroundColor: `${props.currentOption == "Inquiry" ? "white" : ""}`, borderRadius: "10px 10px 0 10px"
        }}>
            <img className={s("image")} src={require("../../assert/letter.png")}/>
            <div className={s("text")}>问询函数据</div>
        </div>

        <div className={s("sidebar-content")} onClick={() => {
            clickSideBar("Annual")
        }} style={{
            backgroundColor: `${props.currentOption == "Annual" ? "white" : ""}`, borderRadius: "10px 0 10px 10px"
        }}>
            <img className={s("image")} src={require("../../assert/book.png")}/>
            <div className={s("text")}>年报数据</div>
        </div>

    </div>)
}

function Content(props) {

    if (props.currentOption == "Inquiry") {
        return <InquiryLetter chartRef={props.chartRef}/>
    } else {
        return <AnnualReport/>
    }
}

//问询函部分
function InquiryLetter(props) {
    const [isChooseFile, setIsChooseFile] = useState(false)
    const [fileName, setFileName] = useState(null)
    const [inquiryFile, setInquiryFile] = useState(null)
    const [inquiryFold, setInquiryFold] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [isFileFold, setIsFileFold] = useState(false)
    const [wordCloudUrl, setWordCloudUrl] = useState("http://finova-wordcloud.oss-cn-guangzhou.aliyuncs.com/ba46a688-4a77-4ad8-a5f5-846f8c7f95a3?Expires=1682667528&OSSAccessKeyId=LTAI5tJMP71xv3KtwuTc9VMn&Signature=YsjUjud2z6xfKd8v%2F4BSdx6VKO8%3D")
    const [isFileAnalysisReady, setIsFileAnalysisReady] = useState(false)

    const [wordArr, setWordArr] = useState([])
    const [probabilityArr, setProbabilityArr] = useState([])

    function chooseInquiryFile(e) {
        console.log(e)
        console.log(isFileFold)
        if (e.target.files.length !== 0) {
            setFileName(e.target.files[0].name)
            setIsChooseFile(true)
            if (e.target.files.length == 1) {
                const formData = new FormData();
                formData.append('file', e.target.files[0]);
                // console.log(formData.get('stockFile'))
                console.log("formData", formData)
                console.log("formData.get('file')", formData.get('file'));
                setInquiryFile(formData.get('file'))
            } else {
                const foldData = new FormData()
                for (let i = 0; i < e.target.files.length; i++) {
                    foldData.append('file', e.target.files[i])
                }
                setInquiryFold(foldData.get('file'))
            }
        }
    }

    async function uploadInquiryFile() {
        let token = getToken()
        console.log(getToken())
        //上传单个文件
        if (!isFileFold) {
            console.log(inquiryFile)
            setIsLoading(true)
            try {
                const res1 = await http.post(`http://${ip}:8002/loads/upload/file`, {
                        file: inquiryFile,
                        uid: token,
                        fileType: 1
                    },
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                )
                console.log("res1", res1)

                console.log("res1.data.data", res1.data.data)
                const fid = res1.data.data

                const res2 = await http.post(`http://${ip}:8002/infoExtractions/extract/inquiry/file?fid=${fid}&algType=1`)
                console.log("res2", res2)
                console.log("res2.data", res2.data)
                // console.log("JSON.parse(res2.data)", JSON.parse(res2.data))

                if (res2.status === 200) {
                    //拿到词云的链接
                    setWordCloudUrl(res2.data.data.png)

                    //拿到包含关键词和概率的json
                    console.log("JSON.parse(res2.data.data.json)", JSON.parse(res2.data.data.json))
                    setProbabilityArr(JSON.parse(res2.data.data.json).possibility)
                    setWordArr(JSON.parse(res2.data.data.json).name)
                }
                setIsLoading(false)
                setIsFileAnalysisReady(true)
            } catch (e) {
                setIsLoading(false)
                message.error("分析失败")
            }

        }
        //上传文件夹
        else {
            console.log("inquiryFold", inquiryFold)
            const res1 = await http.post(`http://${ip}:8002/loads/upload/folder`, {
                    folder: inquiryFold,
                    uid: token,
                    folderType: 1
                },
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                }
            )
            console.log("res1", res1)
            let fid = res1.data.data
            const res2 = await http.post(`http://${ip}:8002/infoExtractions/extract/inquiry/folder?fid=${fid}&algType=2`)
            console.log("res2", res2)
        }

    }


    return (<div className={s("inquiry-box")}>
        <div className={s("up-box")}>
            <div className={s("upload-box")}>
                {
                    !isChooseFile &&
                    <div className={s("upload-button")} onClick={() => {
                        let flag = isFileFold ? false : true
                        setIsFileFold(flag)
                    }}>切换
                    </div>
                }


                <label htmlFor="upload-inquiry-file" style={{cursor: "pointer"}}>
                    {
                        !isChooseFile
                            ?
                            <div className={s("upload-button")} style={{
                                marginLeft: "1vmin"
                            }}>点击此处上传问询函文件{isFileFold && "夹"}</div>
                            :
                            <div className={s("upload-file-box")}>
                                <div className={s("left")}>
                                    <img className={s("image")} src={require("../../assert/blue-file.png")}/>
                                </div>
                                <div className={s("middle")}>
                                    <div className={s("text1")}>
                                        {fileName}{isFileFold && "等"}
                                    </div>
                                    <div className={s("text2")}>
                                        上传完成
                                    </div>
                                </div>
                            </div>
                    }
                </label>
                {
                    isChooseFile &&
                    <div className={s("re-upload-button")} onClick={() => {
                        setIsChooseFile(false)
                        setIsFileAnalysisReady(false)

                    }}>
                        重新上传
                    </div>

                }
                <input type="file" onChange={chooseInquiryFile} id="upload-inquiry-file" name="stockFile"
                       style={{display: "none"}} key={Date.now()}
                    // webkitdirectory={isFileFold ? true : false}
                       webkitdirectory={isFileFold ? "" : false}
                />
            </div>

            <div className={s("extra-button")}
                 style={{
                     background: !isChooseFile ? "#E4E4E4" : "linear-gradient(317.66deg, #45D9AC 0%, #F2BC7D 100%)",
                     cursor: isChooseFile ? "pointer" : ""
                 }}
                 onClick={uploadInquiryFile}
            >
                {!isChooseFile ? "未选择文件" : !isLoading ? "开始提取" : <>提取中<LoadingOutlined/></>}

            </div>

            <div className={s("upload-introduction-box")}>
                <img className={s("back-card")} src={require("../../assert/extraction-card.png")}/>
                <div className={s("introduction-box")}>
                    <div className={s("introduction-content")} style={{
                        width: "11vw"
                    }}>
                        <img className={s("image")} src={require("../../assert/grey-upload.png")}/>
                        <div className={s("text")}>上传问询函文件或文件夹</div>
                    </div>
                    <div className={s("introduction-content")} style={{
                        width: "11.5vw"
                    }}>

                        <img className={s("image")} src={require("../../assert/grey-key.png")}/>
                        <div className={s("text")}>平台分析提取 问询函文件内容</div>
                    </div>
                    <div className={s("introduction-content")} style={{
                        width: "24vw"
                    }}>
                        <img className={s("image")} src={require("../../assert/grey-file.png")}/>
                        <div className={s("textOR")} onClick={() => {
                            console.log(Math.random())
                        }}>OR
                        </div>
                        <img className={s("image")} src={require("../../assert/grey-fold.png")}/>
                        <div className={s("text")}
                        >上传文件后生成词云与柱状图 上传文件夹后会导出表格文件
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {
            !isFileAnalysisReady
                ?
                <div className={s("down-box")}>

                    {/*<img src="http://finova-wordcloud.oss-cn-guangzhou.aliyuncs.com/64562c9c-7206-41f6-aa97-ab56e812f570?Expires=1682656045&OSSAccessKeyId=LTAI5tJMP71xv3KtwuTc9VMn&Signature=f%2Fwtr1yIxCCSJoEHfAy2fkLGAhw%3D"/>*/}

                    <div className={s("first-box")}>
                    <span className={s("left")}>
                        What?
                    </span>
                        <div className={s("text")}>
                            问询函是指证券监管机构向上市公司或其他市场主体发出的一种询问函件，
                            旨在了解有关公司的经营状况、财务情况、内部管理、重大事项等信息。
                            通常是在上市公司或其他市场主体的年度或中期报告披露之后，
                            监管机构认为有必要了解更多信息时才会发出问询函。
                        </div>
                        <div className={s("back-text")}>WHAT</div>

                    </div>

                    <div className={s("second-box")}>
                        <div className={s("left")}>
                            问询函的内容通常是针对上市公司或其他市场主体的具体情况而定，可能包括以下方面：
                        </div>
                        <div className={s("right")}>
                            <div className={s("right-content")}>公司经营业绩、业务发展、市场竞争状况等方面的情况；</div>
                            <div className={s("right-content")}>公司财务状况，包括资产负债表、利润表、现金流量表等方面的情况；</div>
                            <div className={s("right-content")}>公司内部管理、公司治理、公司董事会和监事会等方面的情况；</div>
                            <div className={s("right-content")}>公司重大事项的披露、内幕信息的管理、相关法规的遵守等方面的情况。</div>
                        </div>
                    </div>

                    <div className={s("third-box")}>
                <span className={s("left")}>
                    Which?
                </span>
                        <div className={s("right")}>
                            <div className={s("text1")}>
                                通过批量对问询函进行主题分析和信息提取，可以帮助研究者提高研究效率、
                                提供投资建议和改进研究方法。具体来说在以下方面存在明显价值：
                            </div>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <div className={s("text2")}>深入了解监管趋势：</div>
                                <div className={s("text1")}>
                                    通过对大量问询函进行主题分析，
                                    金融研究者可以深入了解监管部门的关注点和监管趋势，
                                    及时掌握市场动态。
                                </div>
                            </div>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <div className={s("text2")}>建立监管模型：</div>
                                <div className={s("text1")}>
                                    通过对问询函主题的研究，金融研究者可以建立监管模型，对监管趋势进行预测和分析，为企业和投资者提供参考和决策依据。
                                </div>
                            </div>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <div className={s("text2")}>提高研究效率：</div>
                                <div className={s("text1")}>
                                    批量问询函主题分析可以帮助金融研究者快速定位监管部门的重点问题和关注点，提高研究效率和准确性。
                                </div>
                            </div>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <div className={s("text2")}>提供投资建议：</div>
                                <div className={s("text1")}>
                                    通过对问询函主题的研究，金融研究者可以提供投资建议，为投资者提供有价值的市场分析和投资参考。
                                </div>
                            </div>
                            <div style={{display: "flex", flexDirection: "row"}}>
                                <div className={s("text2")}>改进研究方法：</div>
                                <div className={s("text1")}>
                                    批量问询函主题分析可以帮助金融研究者更加深入地了解监管环境和监管要求，及时调整和改进研究方法，提高研究水平和质量。
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className={s("fourth-box")}>
                <span className={s("left")}>
                    How?
                </span>
                        <div className={s("right")}>
                            例：该模块通过爬取深圳证券交易所近年来6617份问询函，进行LDA主题分析，
                            自动地从文本数据中提取出主题，并对文本数据中的潜在关系和模式进行了深入挖掘，
                            为进一步的分析和应用提供了基础。具体来说，通过LDA模型的训练，
                            我们提炼出了问询函的10大主题，
                            具体包括，收入与业绩（32.7%），借款担保（4.4%），产品市场（4.1%）等。每个主题提取出前25个关键词，
                            如收入与业绩主题的关键词有业务，应收账款，营业收入，显示，下降等。
                        </div>
                    </div>

                    <div className={s("fifth-box")}>
                        <div className={s("fifth-box-content")}>
                            <img className={s("image")} src={require("../../assert/grey-uploadfile.png")}/>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <img className={s("image")} src={require("../../assert/grey-uploadfold.png")}/>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <div className={s("text1")}>
                                上传
                                <span className={s("text2")}>问询函文件</span>
                                或
                                <span className={s("text2")}>文件夹</span>
                            </div>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <img className={s("image")} src={require("../../assert/grey-arrow-right.png")}/>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <img className={s("image")} src={require("../../assert/grey-histogram.png")}/>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <img className={s("image")} src={require("../../assert/grey-wordcloud.png")}/>
                        </div>
                        <div className={s("fifth-box-content")}>
                            <div className={s("text1")}>
                                生成
                                <span className={s("text2")}>柱状图</span>
                                与
                                <span className={s("text2")}>词云</span>
                            </div>
                        </div>
                    </div>

                    <div className={s("six-box")}>
                        用户可以上传需要分析的问询函，系统为用户分析出该问询函所属主题，
                        并返回该问询函的词云帮助用户更快速的提取问询函的进一步信息。
                        用户也可以批量上传问询函，我们会为用户批量进去主题提取。
                        用户也可以选择使用自己上传的问询函重新训练LDA模型。
                    </div>
                </div>
                :
                <div className={s("down-box")} style={{
                    display: "flex", flexDirection: "row"
                }}>
                    <div className={s("cloud-left")}>
                        <img className={s("image")} src={wordCloudUrl}/>
                    </div>
                    <div><Histogram wordArr={wordArr} probabilityArr={probabilityArr}/></div>
                </div>
        }
    </div>)
}

//------------------------------------------------------------------
//年报部分

function AnnualSideBar(props) {
    function AnnualclickSideBar(option) {
        props.AnnualclickSideBarItem(option)
    }

    return (
        <div className={s("annualsidebar-box")}>
            <div className={s("sidebar-content")} onClick={() => {
                AnnualclickSideBar("Service")
            }} style={{
                backgroundColor: `${props.currentOption == "Service" ? "white" : ""}`, borderRadius: "10px 10px 0 10px"
            }}>

                <div className={s("text")}>营运能力</div>
            </div>

            <div className={s("sidebar-content")} onClick={() => {
                AnnualclickSideBar("Profit")
            }} style={{
                backgroundColor: `${props.currentOption == "Profit" ? "white" : ""}`, borderRadius: "10px 0 10px 10px"
            }}>

                <div className={s("text")}>盈利能力</div>
            </div>

            <div className={s("sidebar-content")} onClick={() => {
                AnnualclickSideBar("Debt")
            }} style={{
                backgroundColor: `${props.currentOption == "Debt" ? "white" : ""}`, borderRadius: "10px 0 10px 10px"
            }}>

                <div className={s("text")}>偿债能力</div>
            </div>

            <div className={s("sidebar-content")} onClick={() => {
                AnnualclickSideBar("Develop")
            }} style={{
                backgroundColor: `${props.currentOption == "Develop" ? "white" : ""}`, borderRadius: "10px 0 10px 10px"
            }}>

                <div className={s("text")}>发展能力</div>
            </div>

        </div>)
}

const Service1 = [
    '库存周转率： ',
    '应收账款周转率：',
    '总资产周转率：',
    '现金流量比率∶',
    '存货周转天数：',
    '应收账款周转天数：'
]

const Service2 = [
    '库存周转率=销售收入÷[(期初存货＋期末存货)÷2]',
    '应收账款周转率=营业收入÷[(期初应收账款+期末应收账款)÷2]',
    '总资产周转率=营业收入÷[(期初总资产+期末总资产)÷2]',
    '现金流量比率 = 经营活动现金流量净额÷净营业收入',
    '存货周转天数=[(期初存货+期末存货)÷2]÷(年度销售成本÷365)',
    '应收账款周转天数=[(期初应收账款+期末应收账款)÷(年度确信收入÷365)',
]

function Service() {
    const [hoveredIndex, setHoveredIndex] = useState(null);
    const [hoveredIndex1, setHoveredIndex1] = useState(null);

    return (
        <div className={s("Common_List")}>
            <List
                className={s("textul")}
                bordered
                dataSource={[...Service1.keys()]}
                renderItem={(index) => (
                    <List.Item
                        className={s("textlist")}
                        onMouseEnter={() => setHoveredIndex(index)}
                        onMouseLeave={() => setHoveredIndex(null)}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            position: "relative",
                            backgroundColor: hoveredIndex === index ? "lightgray" : "",
                            fontWeight: hoveredIndex === index ? "550" : "400",
                        }}
                    >
              <span className={s("textleft")} style={{flex: 1}}>
                <Typography.Text mark></Typography.Text> {Service1[index]}
              </span>
                        <span
                            className={s("textcenter")}
                            style={{
                                flex: 1,
                                textAlign: "center",
                                whiteSpace: "nowrap",
                            }}
                        >
                <Typography.Text></Typography.Text>{Service2[index]}
              </span>
                        <div
                            className={s("textright")}
                            style={{flex: 1, textAlign: "right"}}
                        >
                            <Tooltip
                                title="你好，很高兴认识你"
                                visible={hoveredIndex1 === index}
                            >
                                <img
                                    className={s("img1")}
                                    onMouseEnter={() => {
                                        setHoveredIndex1(index);
                                    }}
                                    onMouseLeave={() => {
                                        setHoveredIndex1(null);
                                    }}
                                    src={require("../../assert/Group.png")}
                                    style={{
                                        filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                    }}
                                />
                            </Tooltip>

                            <img
                                className={s("img2")}
                                onMouseEnter={() => setHoveredIndex1(index)}
                                onMouseLeave={() => setHoveredIndex1(null)}
                                src={require("../../assert/_.png")}
                                style={{
                                    filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                }}
                            />
                        </div>
                    </List.Item>
                )}
                style={{borderLeft: "none", borderRight: "none"}} // 设置样式
            />
        </div>
    );
}

const Profit1 = [
    '毛利率： ',
    '净利率：',
    '营业利润率：',
    '总资产收益率：',
    '每股收益：',

]

const Profit2 = [
    '毛利率 =(销售收入 - 销售成本)÷ 销售收入',
    '净利率 = 净利润 ÷ 销售收入',
    '营业利润率 = 营业利润 ÷ 销售收入',
    '总资产收益率 = 净利润 ÷ [(期初总资产 ＋ 期末总资产)÷ 2]',
    '每股收益=净利润 ÷加权平均股本',

]

function Profit() {
    const [hoveredIndex, setHoveredIndex] = useState(null);
    const [hoveredIndex1, setHoveredIndex1] = useState(null);

    return (
        <div className={s("Common_List")}>
            <List
                className={s("textul")}
                bordered
                dataSource={[...Profit1.keys()]}
                renderItem={(index) => (
                    <List.Item
                        className={s("textlist")}
                        onMouseEnter={() => setHoveredIndex(index)}
                        onMouseLeave={() => setHoveredIndex(null)}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            position: "relative",
                            backgroundColor: hoveredIndex === index ? "lightgray" : "",
                            fontWeight: hoveredIndex === index ? "550" : "400",
                        }}
                    >
              <span className={s("textleft")} style={{flex: 1}}>
                <Typography.Text mark></Typography.Text> {Service1[index]}
              </span>
                        <span
                            className={s("textcenter")}
                            style={{
                                flex: 1,
                                textAlign: "center",
                                whiteSpace: "nowrap",
                            }}
                        >
                <Typography.Text></Typography.Text>{Service2[index]}
              </span>
                        <div
                            className={s("textright")}
                            style={{flex: 1, textAlign: "right"}}
                        >
                            <Tooltip
                                title="你好，很高兴认识你"
                                visible={hoveredIndex1 === index}
                            >
                                <img
                                    className={s("img1")}
                                    onMouseEnter={() => {
                                        setHoveredIndex1(index);
                                    }}
                                    onMouseLeave={() => {
                                        setHoveredIndex1(null);
                                    }}
                                    src={require("../../assert/Group.png")}
                                    style={{
                                        filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                    }}
                                />
                            </Tooltip>

                            <img
                                className={s("img2")}
                                onMouseEnter={() => setHoveredIndex1(index)}
                                onMouseLeave={() => setHoveredIndex1(null)}
                                src={require("../../assert/_.png")}
                                style={{
                                    filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                }}
                            />
                        </div>
                    </List.Item>
                )}
                style={{borderLeft: "none", borderRight: "none"}} // 设置样式
            />
        </div>
    );
}

const Debt1 = [
    '流动比率： ',
    '速动比率：',
    '负债总额与净资产比率：',


]

const Debt2 = [
    '流动比率 =流动资产÷流动负债',
    '速动比率=（流动资产-存货）÷流动负债',
    '负债总额与净资产比率 = 负债总额 ÷ 净资产',
]

function Debt() {
    const [hoveredIndex, setHoveredIndex] = useState(null);
    const [hoveredIndex1, setHoveredIndex1] = useState(null);

    return (
        <div className={s("Common_List")}>
            <List
                className={s("textul")}
                bordered
                dataSource={[...Debt1.keys()]}
                renderItem={(index) => (
                    <List.Item
                        className={s("textlist")}
                        onMouseEnter={() => setHoveredIndex(index)}
                        onMouseLeave={() => setHoveredIndex(null)}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            position: "relative",
                            backgroundColor: hoveredIndex === index ? "lightgray" : "",
                            fontWeight: hoveredIndex === index ? "550" : "400",
                        }}
                    >
              <span className={s("textleft")} style={{flex: 1}}>
                <Typography.Text mark></Typography.Text> {Service1[index]}
              </span>
                        <span
                            className={s("textcenter")}
                            style={{
                                flex: 1,
                                textAlign: "center",
                                whiteSpace: "nowrap",
                            }}
                        >
                <Typography.Text></Typography.Text>{Service2[index]}
              </span>
                        <div
                            className={s("textright")}
                            style={{flex: 1, textAlign: "right"}}
                        >
                            <Tooltip
                                title="你好，很高兴认识你"
                                visible={hoveredIndex1 === index}
                            >
                                <img
                                    className={s("img1")}
                                    onMouseEnter={() => {
                                        setHoveredIndex1(index);
                                    }}
                                    onMouseLeave={() => {
                                        setHoveredIndex1(null);
                                    }}
                                    src={require("../../assert/Group.png")}
                                    style={{
                                        filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                    }}
                                />
                            </Tooltip>

                            <img
                                className={s("img2")}
                                onMouseEnter={() => setHoveredIndex1(index)}
                                onMouseLeave={() => setHoveredIndex1(null)}
                                src={require("../../assert/_.png")}
                                style={{
                                    filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                }}
                            />
                        </div>
                    </List.Item>
                )}
                style={{borderLeft: "none", borderRight: "none"}} // 设置样式
            />
        </div>
    );
}

const Develop1 = [
    '固定资产周转率： ',
    '研发费用率：',
    '资产负债率：',
    '现金再投资比率:',
]

const Develop2 = [
    '固定资产周转率 = 营业收入 ÷[(期初固定资产 ＋ 期末固定资产)÷ 2]',
    '研发费用率 = 研发费用÷营业收入',
    '资产负债率 = 负债总额 ÷ 总资产',
    '现金再投资比率=经营活动现金流量净额 ÷ 投资活动现金流量净额',
]

function Develop() {
    const [hoveredIndex, setHoveredIndex] = useState(null);
    const [hoveredIndex1, setHoveredIndex1] = useState(null);

    return (
        <div className={s("Common_List")}>
            <List
                className={s("textul")}
                bordered
                dataSource={[...Develop1.keys()]}
                renderItem={(index) => (
                    <List.Item
                        className={s("textlist")}
                        onMouseEnter={() => setHoveredIndex(index)}
                        onMouseLeave={() => setHoveredIndex(null)}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            position: "relative",
                            backgroundColor: hoveredIndex === index ? "lightgray" : "",
                            fontWeight: hoveredIndex === index ? "550" : "400",
                        }}
                    >
              <span className={s("textleft")} style={{flex: 1}}>
                <Typography.Text mark></Typography.Text> {Service1[index]}
              </span>
                        <span
                            className={s("textcenter")}
                            style={{
                                flex: 1,
                                textAlign: "center",
                                whiteSpace: "nowrap",
                            }}
                        >
                <Typography.Text></Typography.Text>{Service2[index]}
              </span>
                        <div
                            className={s("textright")}
                            style={{flex: 1, textAlign: "right"}}
                        >
                            <Tooltip
                                title="你好，很高兴认识你"
                                visible={hoveredIndex1 === index}
                            >
                                <img
                                    className={s("img1")}
                                    onMouseEnter={() => {
                                        setHoveredIndex1(index);
                                    }}
                                    onMouseLeave={() => {
                                        setHoveredIndex1(null);
                                    }}
                                    src={require("../../assert/Group.png")}
                                    style={{
                                        filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                    }}
                                />
                            </Tooltip>

                            <img
                                className={s("img2")}
                                onMouseEnter={() => setHoveredIndex1(index)}
                                onMouseLeave={() => setHoveredIndex1(null)}
                                src={require("../../assert/_.png")}
                                style={{
                                    filter: hoveredIndex1 === index ? "brightness(3)" : "",
                                }}
                            />
                        </div>
                    </List.Item>
                )}
                style={{borderLeft: "none", borderRight: "none"}} // 设置样式
            />
        </div>
    );
}

function AnnualContent(props) {
    if (props.currentOption == "Develop") {
        return <Develop/>
    } else if (props.currentOption == "Profit") {
        return <Profit/>
    } else if (props.currentOption == "Debt") {
        return <Debt/>
    } else {
        return <Service/>
    }
}

function AnnualReport() {
    const [contentOption, setContentOption] = useState("Service")

    function changeContentOption(option) {
        setContentOption(option)
    }

    const [divId, setDivId] = useState('default')//按钮的切换是这个，newDiv和default切换
    // const [divId, setDivId] = useState('newDiv')
    return (
        <div className={s("annual-box")}>
            <div className={s("annual-up-box")}>
                <div className={s("annual-upload-box1")}>
                    这里上传文件
                </div>
                <div className={s("annual-upload-box2")}>
                    这里上传文件
                </div>
                <div className={s("annual-upload-box3")}>
                    这里上传文件
                </div>

                <div className={s("annual-extra-button")}>
                    未上传文件
                </div>


            </div>

            {divId === 'default' && <div id="default" className={s("annual-down-box1")}>
                <div className={s("annual-first-box")}>
                <span className={s("annual-left")}>
                    Which?
                </span>
                    <div className={s("annual-text")} style={{lineHeight: '1'}}>

                        <p> 资产负债表、现金流量表和利润表是企业财务报表中的三个主要部分，三个表报从不同的方面评估企业的情况，具体来说：</p>
                        <p><span style={{fontWeight: 'bold'}}>资产负债表：</span>资产负债表是企业财务报表的核心部分，用于展示企业在某一时点的资产、负债和所有者权益情况。通过分析资产负债表，可以评估
                        </p>
                        <p>企业的偿债能力、流动性和资本结构，并确定企业的财务稳健程度。</p>
                        <p><span style={{fontWeight: 'bold'}}>现金流量表：</span>现金流量表用于展示企业在某一期间内的现金流入和流出情况。通过分析现金流量表，可以评估企业的现金流量状况、经营能力和资
                        </p>
                        <p>金利用效率，并确定企业的财务稳健程度。</p>
                        <p><span style={{fontWeight: 'bold'}}>利润表：</span>利润表展示了企业在某一期间内的收入、成本和利润情况。通过分析利润表，可以评估企业的盈利能力、经营效率和财务状况，并确定企
                        </p>
                        <p>业的发展潜力和风险程度。</p>

                    </div>
                    <div className={s("annual-back-text")}>WHICH</div>

                </div>

                <div className={s("annual-second-box")}>

                    <div className={s("annual-second-box-content")}>
                        <img className={s("image")} src={require("../../assert/grey-uploadfile.png")}/>
                    </div>
                    <div className={s("annual-second-box-content")}>
                        <img className={s("image")} src={require("../../assert/Cross.png")}/>
                    </div>
                    <div className={s("annual-second-box-content")}>
                        <img className={s("image")} src={require("../../assert/3.png")}/>
                    </div>
                    <div className={s("annual-second-box-content")}>
                        <div className={s("text1")}>
                            上传
                            <span className={s("text2")}>三份年报文件</span>

                        </div>
                    </div>
                    <div className={s("annual-second-box-content")}>
                        <img className={s("image")} src={require("../../assert/grey-arrow-right.png")}/>
                    </div>
                    
                    <div className={s("annual-second-box-content")}>
                        <img className={s("image")} src={require("../../assert/Cube.png")}/>
                    </div>
                    <div className={s("annual-second-box-content")}>
                        <div className={s("text1")}>
                            分析
                            <span className={s("text2")}>四大能力</span>
                            与其
                            <span className={s("text2")}>数据内容</span>
                        </div>
                    </div>


                </div>


                <div className={s("annual-third-box")}>
                <span className={s("annual-left")}>

                    How?
                </span>
                    <div className={s("annual-text")} style={{lineHeight: '1'}}>


                        <p> 批量分析年报上的各种数据，从横向上看，批量分析可以帮助金融研究者更快速地了解和比较不同公司在某个指标上的表现。通过将不同公司的数</p>
                        <p>据整合在一起，可以更容易地进行比较和分析。</p>
                        <p>此外，批量分析也可以帮助金融研究者快速筛选出表现较好的公司，以便更加精准地进行进一步的分析和投资决策。</p>
                        <p>从纵向上看，批量分析可以帮助金融研究者深入了解某家特定的公司。例如，通过计算公司的营业利润率、净利润率、总资产周转率等指标的变化</p>
                        <p>情况，可以评估其盈利能力、资产利用效率等方面的表现。</p>
                        <p>该模块允许用户批量上传企业的财务报表，具体包括资产负债表，现金流量表和利润表，系统可以自动提取用户上传的报表中的相关表项信息，从</p>
                        <p><span style={{fontWeight: 'bold'}}>营运能力，盈利能力，发展能力，偿债能力</span>等四个方面对企业的情况进行分析，方便金融研究者快速从整体把握企业的具体情况。
                        </p>

                    </div>
                    <div className={s("annual-back-text")}>HOW</div>

                </div>


            </div>}

            {divId === 'newDiv' &&
                <div id="newDiv" className={s("annual-down-box2")}>

                    <AnnualSideBar AnnualclickSideBarItem={changeContentOption} currentOption={contentOption}/>
                    <div className={s("content-box")}>
                        <AnnualContent currentOption={contentOption}/>
                    </div>
                </div>
            }
        </div>

    )
}

function Extraction() {
    const [contentOption, setContentOption] = useState("Inquiry")

    function changeContentOption(option) {
        setContentOption(option)
    }


    return (<div className={s("content-box")}>
        <div className={s("back-box")}>
            <img src={require("../../assert/extraction-back.png")} className={s("back-cover-img")}/>
            <div className={s("back-cover")}></div>
        </div>

        <div className={s("introduce-box")}>
            <div className={s("title-box")}>
                <div className={s("title")}>信息抽取</div>
                <div className={s("title-english")}>Information extraction</div>
            </div>

            <div className={s("text-box")}>
                <div className={s("text")}>
                    该模块允许用户上传并分析各种文件，例如问询函、年报等，
                    并从中提取出关键信息。 我们通过数据挖掘技术和自然语言处理技术，
                    从文件中获取有用的信息和数据，帮助用户更好地做出决策。
                </div>
            </div>
        </div>

        <div className={s("bottom-box")}>
            <SideBar clickSideBarItem={changeContentOption} currentOption={contentOption}/>
            <div className={s("content-box")}>
                <Content currentOption={contentOption}/>
            </div>
        </div>
    </div>)
}

export default Extraction
