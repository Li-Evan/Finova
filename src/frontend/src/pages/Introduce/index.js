import {Form, Input, Checkbox, Button, message, Layout, Menu} from "antd";
import {useStore} from "../../store";
import style from "./index.module.css";
// import "./index.module.css"
import {getToken} from "../../utils";
import {
    HomeOutlined,
    DiffOutlined,
    EditOutlined,

} from '@ant-design/icons'
import {ip} from "../../constIp"

import {makeStyle} from "../../utils/CSSUtils";


// import "../.././assert/black-logo.png";
import {http} from "../../utils";
import {useNavigate, useLocation, Link} from "react-router-dom";
import {useState, useEffect} from "react";
import SubMenu from "antd/es/menu/SubMenu";

const {Header, Content, Footer} = Layout;

const s = makeStyle(style)


function Platform_Introduction() {
    return (
        <div className={s("introduce-box")}>
            <div className={s("introduce-title")}>
                <span className={s("text1")}>平台介绍</span>
                <span className={s("text2")}>Introduce</span>
            </div>

            <div className={s("introduce-content-box")}>
                <div className={s("content-first")}>
                    欢迎来到<span className={s("text")}>FINOVA</span>!
                </div>
                <div className={s("content-second")}>
                    Finova由"Fin"和"nova"两个单词组成，
                    "Fin"代表着金融，而"nova"则代表着新星、新生和新的开始。
                    我们的平台旨在通过创新的方式，用技术为金融赋能，为金融提供更多的可能。
                </div>
                <div className={s("content-third")}>
                    <img style={{height:"7vmin"}} src={require("../../assert/black-logo.png")}/>
                    <div className={s("right")}>
                        <div className={s("text")}>运筹帷幄之中，决胜千里之外。</div>
                        <img src={require("../../assert/black-signature.png")}/>
                    </div>
                </div>
                <div className={s("content-fourth")}>
                    我们平台希望能够同时为专业投资者和金融新手赋能，我们为每个模块提供了详细的介绍和详细的解释，希望能够让金融新手快速入门。
                </div>
                <div className={s("content-fifth")}>
                    <div className={s("content-fifth-content")}>
                        <div className={s("left")}>
                            <img src={require("../../assert/chart.png")} className={s("image")}/>
                            <div className={s("text")}>量化</div>
                        </div>
                        <div className={s("right")}>
                            我们提供了多种的量化交易模型，方便专业投资者进行回测和预测。
                            同时，我们也允许用户上传自己的量化交易模型，我们会为基于用户上传的模型进行回测。
                        </div>
                    </div>
                    <div className={s("content-fifth-content")}>
                        <div className={s("left")}>
                            <img src={require("../../assert/key.png")} style={{width: "5vmin", height: "3.5vmin"}}/>
                            <div className={s("text")}>数据</div>
                        </div>
                        <div className={s("right")}>
                            我们同时提供了信息批量提取的功能，希望在这个信息纷繁的金融世界，为用户筑起一道过滤的屏障。
                        </div>
                    </div>

                </div>
                <div className={s("content-sixth")}>
                    我们期待与您一起探索这个充满机遇的市场，成为您量化投资过程中的好帮手，为您提供优质的交易体验，让我们出发吧！
                </div>
            </div>

            <div className={s("back-text")}>INTRODUCE</div>

        </div>
    );
}

function Platform_Introduction_Quantify() {
    return (
        <div className={s("introduce-box")}>
            <div className={s("introduce-title")}>
                <span className={s("text1")}>量化交易</span>
                <span className={s("text2")}>Quantitative Trading</span>
            </div>
            <div className={s("introduce-quantify-content-box")}>
                <div className={s("up")}>
                    <div className={s("left")}>
                        <img src={require("../../assert/chart.png")} className={s("image")}/>
                        <span className={s("text1")}>量化</span>
                        <span className={s("text2")}>交易的数据可视化</span>
                    </div>
                    <div className={s("right")}>
                        该模块提供各种量化交易的模型，将模型应用到某个股票上之后，
                        由模型算出的买入和卖出日期。用户可以通过该模块获取股票市场的各种交易策略。
                        我们的平台将提供丰富的数据分析工具，帮助用户分析股票市场的行情，
                        以及判断买卖时机等重要因素。 具体数据会以动态折线图的方式呈现：
                    </div>
                </div>
                <div className={s("down")}>
                    <img src={require("../../assert/quantify-introduction.png")} className={s("image")}/>
                    <div className={s("button-box")}>
                        {/*<div className={s("button-content")} onClick={() => handleItemClick('Manual-Quantify')}>*/}
                        {/*    <div className={s("text1")}>使用方法</div>*/}
                        {/*    <div className={s("text2")}>How to use</div>*/}
                        {/*    <div className={s("arrow-box")}>*/}
                        {/*        <img className={s("arrow")} src={require("../../assert/arrow-right.png")}/>*/}
                        {/*    </div>*/}
                        {/*</div>*/}
                        <Link className={s("button-content")} to={"/quantify"}>
                            <div className={s("text1")}>立即使用</div>
                            <div className={s("text2")}>Use it now</div>
                            <div className={s("arrow-box")}>
                                <img className={s("arrow")} src={require("../../assert/arrow-right.png")}/>
                            </div>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

function Platform_Introduction_Extraction() {
    return (
        <div className={s("introduce-box")}>
            <div className={s("introduce-title")}>
                <span className={s("text1")}>信息抽取</span>
                <span className={s("text2")}>Information Extraction</span>
            </div>
            <div className={s("introduce-extraction-content-box")}>
                该模块提供各种量化交易的模型，将模型应用到某个股票上之后，
                由模型算出的买入和卖出日期。 用户可以通过该模块获取股票市场的各种交易策略。
                我们的平台将提供丰富的数据分析工具，帮助用户分析股票市场的行情，
                以及判断买卖时机等重要因素。
            </div>

            <div style={{
                fontFamily: 'PingFang SC',
                fontStyle: "normal",
                fontWeight: "800",
                fontSize: "20vmin",
                marginTop: "20vmin",
                //margin-left: 30vmin;
                color: "rgba(0, 0, 0, 0.03)",
            }}>INTRODUCE
            </div>

        </div>
    )
}

function Operating_Manual() {
    return (
        <div className={s("introduce-box")} style={{
            height: "90vh", overflow: "hidden",
            overflowY: "scroll"
        }}>
            <div className={s("introduce-title")}>
                <span className={s("text1")}>操作手册</span>
                <span className={s("text2")}>Operation Manual</span>
            </div>
            <div className={s("manual-box")}>
                <div className={s("manual-content")}>
                    <div className={s("text")}>1、 访问Finova社区门户，点击右上角“登录”</div>
                    <div className={s("text")}>
                        填入相应的信息，Finova提供两种登录注册方式。
                        第一种是用户名+密码注册登录，第二种是手机号+验证码登录。
                        {/*输入正确的手机号码之后，点击“发送验证码”，*/}
                        {/*可以收到验证码，填入后点击“登录”按钮。*/}
                    </div>
                    <img className={s("image")} src={require("../../assert/manual1.png")}/>
                </div>
                <div className={s("manual-content")}>
                    <div className={s("text")}>2.1 用户名+密码注册</div>
                    <div className={s("text")}>
                        输入未在数据库中注册的用户名，重复输入相同密码两次，即可完成注册。
                        密码要求至少出现大写字母，小写字母，数字，特殊符号中的至少两种，且长度至少为8位。
                    </div>
                    <img className={s("image")} src={require("../../assert/manual2.png")}/>
                </div>
                <div className={s("manual-content")}>
                    <div className={s("text")}>2.2 用户名+密码登录</div>
                    <div className={s("text")}>
                        输入已注册的用户信息，点击登录进入平台。
                    </div>
                    <img className={s("image")} src={require("../../assert/manual3.png")}/>
                </div>
                <div className={s("manual-content")}>
                    <div className={s("text")}>2.3 手机号+验证码登录</div>
                    <div className={s("text")}>
                        输入正确的手机号码之后，点击“发送验证码”，
                        可以收到验证码，填入后点击“登录”按钮。
                    </div>
                    <img className={s("image")} src={require("../../assert/manual4.png")}/>
                </div>
                <div className={s("manual-content")}>
                    <div className={s("text")}>3、登录后跳入首页，即可检测是否登录注册成功。</div>
                    <div className={s("text")}>
                        登录成功后会解锁系统完整功能，如下图所示：
                    </div>
                    <img className={s("image")} src={require("../../assert/manual5.png")}/>
                </div>

            </div>
            <div style={{
                fontFamily: 'PingFang SC',
                fontStyle: "normal",
                fontWeight: "800",
                fontSize: "15vmin",
                marginTop: "-10vmin",
                // margin-left: 30vmin;
                color: "rgba(0, 0, 0, 0.03)",
            }}>Operation Manual
            </div>
        </div>
    );
}

function Operating_Manual_Quantify() {
    return (
        <div className={s("introduce-box")} style={{
            height: "90vh", overflow: "hidden",
            overflowY: "scroll"
        }}>
            <div className={s("introduce-title")}>
                <span className={s("text1")}>量化交易</span>
                <span className={s("text2")}>Quantitative Trading</span>
            </div>
            <div className={s("manual-quantify-box")}>
                <div className={s("top-text-box")}>
                    <div className={s("text")}>
                        该模块提供各种量化交易的模型，将模型应用到某个股票上之后，由模型算出的买入和卖出日期。
                        用户可以通过该模块获取股票市场的各种交易策略。我们的平台将提供丰富的数据分析工具，
                        帮助用户分析股票市场的行情，以及判断买卖时机等重要因素。
                    </div>
                    <div className={s("text")}>
                        初次进入界面，会有两个供您选择的模块，
                        第一模块为选择模型，在这里我们提供了丰富的数据分析模型；
                        第二模块为选择股票，在此模块您可以选择我们所提供的股票文件，也可以选择上传您所拥有的股票文件。
                    </div>
                </div>

                <div className={s("top-img-box")}>
                    <div className={s("top-img-content")}>
                        <img className={s("image")} src={require("../../assert/manual6.png")}/>
                        <div className={s("text")}>选择模型模块</div>
                        <div className={s("text")}>Selective model module</div>
                    </div>
                    <div className={s("top-img-content")}>
                        <img className={s("image")} src={require("../../assert/manual7.png")}/>
                        <div className={s("text")}>选择股票模块</div>
                        <div className={s("text")}>Stock selection module</div>
                    </div>
                </div>

                <div className={s("bottom-box")}>
                    <div className={s("img-box")}>
                        <img className={s("image")} src={require("../../assert/model-icon.png")}/>
                    </div>
                    <div className={s("bottom-text-content")}>
                        <div className={s("title")}>Bollinger模型</div>
                        <div className={s("text")}>
                            Bollinger模型基于统计学原理，用来衡量价格波动性的程度。
                            该算法利用移动平均线和标准差来计算价格的上下限，并将价格的波动范围限定在这个范围内。
                            当价格越过布林带的上限或下限时，这通常意味着价格即将回归到移动平均线附近，
                            从而为交易者提供了进出场的信号。
                        </div>
                    </div>
                    <div className={s("bottom-text-content")}>
                        <div className={s("title")}>Momentum模型</div>
                        <div className={s("text")}>
                            Momentum模型基于市场价格趋势的惯性原理，即在短期内价格的涨跌趋势可能会延续到未来一段时间内。
                            动量模型通过分析市场价格的历史走势，寻找市场的趋势，并根据趋势的方向做出买入或卖出的决策。
                            通常来说，动量模型会使用某一段时间内的价格涨跌幅度作为指标来评估市场的趋势，
                            但当市场出现大的转折时，动量模型可能会失效。
                            此外，过度追求短期趋势的投资者也可能会面临过度交易的风险。
                        </div>
                    </div>
                    <div className={s("bottom-text-content")}>
                        <div className={s("title")}>MACD模型</div>
                        <div className={s("text")}>
                            MACD模型是一种广泛使用的量化交易策略，其基于移动平均线的计算方法，
                            用于分析价格趋势和市场信号。该模型的核心是计算两条移动平均线之间的差值，
                            并绘制出一条叫做“信号线”的移动平均线。当短期均线上穿长期均线并且MACD柱子变成正值时，
                            被视为买入信号；当短期均线下穿长期均线并且MACD柱子变成负值时，被视为卖出信号。
                        </div>
                    </div>
                    <div className={s("bottom-text-content")}>
                        <div className={s("title")}>DMA 模型</div>
                        <div className={s("text")}>
                            DMA 模型的基本思想是通过计算两条不同时间周期的移动平均线来判断市场趋势，
                            从而确定交易信号。具体而言，双均线策略通常会计算一个较短期的移动平均线和一个较长期的移动平均线，
                            当短期均线上穿长期均线时，视为“金叉”信号，买入股票；当短期均线下穿长期均线时，
                            视为“死叉”信号，卖出股票。双均线策略通过较简单的技术指标实现了交易信号的自动化，
                            常用于短期交易和中长期投资。
                        </div>
                    </div>
                    <div className={s("chart-logo-box")}>
                        <img className={s("image")} src={require("../../assert/chart.png")}/>
                        <div className={s("text")}>使用模型分析后的具体数据会以动态折线图的方式呈现：</div>
                    </div>
                    <img src={require("../../assert/quantify-introduction.png")} style={{width:"95%"}}/>
                </div>
            </div>
        </div>
    )
}

function Platform_Services() {
    return (
        <div>
            <h1>平台服务</h1>
        </div>
    );
}

function NewSidebar(props) {

    function handleItemClick(option) {
        props.onOptionChange(option);
    }

    return (
        <div className={s("sidebar")}>
            <Menu
                className={s("test")}
                mode="inline"
                style={{height: '100%', borderRight: 0}}
            >
                <SubMenu title={<div onClick={() => handleItemClick('Introduction')}>平台介绍</div>}>
                    <Menu.Item onClick={() => handleItemClick('Introduction-Quantify')}>
                        量化交易
                    </Menu.Item>
                    <Menu.Item onClick={() => handleItemClick('Introduction-Extraction')}>
                        信息抽取
                    </Menu.Item>
                </SubMenu>
                {/*<Menu.Item*/}
                {/* */}
                {/*  onClick={() => handleItemClick('Introduction')}*/}
                {/*  style={{ backgroundColor: props.selectedOption === 'Introduction' ? '#f5f5f5' : '' }}*/}
                {/*>*/}
                {/*  平台介绍*/}
                {/*</Menu.Item>*/}
                <SubMenu title={<div onClick={() => handleItemClick('Manual')}>操作手册</div>}>
                    <Menu.Item onClick={() => handleItemClick('Manual-Quantify')}>
                        使用-量化交易
                    </Menu.Item>
                    <Menu.Item onClick={() => handleItemClick('Manual-Extraction')}>
                        使用-信息抽取
                    </Menu.Item>
                </SubMenu>
                <Menu.Item

                    onClick={() => handleItemClick('Services')}
                    style={{backgroundColor: props.selectedOption === 'Services' ? '#f5f5f5' : ''}}
                >
                    平台服务
                </Menu.Item>
            </Menu>
        </div>
    );
}

// Platform_Introduction
function NewContent(props) {
    let content;
    if (props.currentOption === 'Introduction') {
        content = <Platform_Introduction/>;
    } else if (props.currentOption === 'Introduction-Quantify') {
        content = <Platform_Introduction_Quantify/>;
    } else if (props.currentOption === 'Introduction-Extraction') {
        content = <Platform_Introduction_Extraction/>;
    } else if (props.currentOption === 'Manual') {
        content = <Operating_Manual/>;
    } else if (props.currentOption === 'Manual-Quantify') {
        content = <Operating_Manual_Quantify/>;
    } else if (props.currentOption === 'Manual-Extraction') {
        content = <Operating_Manual/>;
    } else {
        content = <Platform_Services/>;
    }

    return (
        <div className={s("content")}>

            {content}
        </div>
    );
}

// function NewHeader()
// {
//     const {loginStore} = useStore()
//     const navigate = useNavigate()
//     const {pathname} = useLocation()
//     const [loginWay, setLoginWay] = useState(true)//true代表用户名密码登录，false代表手机验证码登录
//     const [phoneNum, setPhoneNum] = useState("")
//     const [countdown, setCountdown] = useState(0)
//     const [countdownEndTime, setCountdownEndTime] = useState(0)
//     const token = getToken()
//
//     const [form] = Form.useForm();
//
//     return (
//         <div className="Header">
//          <Header className={s("header-box")}>
//                 <div className={s("header-content")}>
//                     <img src={require("../.././assert/black-logo.png")}/>
//                     <div className={s("right")}>
//                         <Menu mode="horizontal"
//                               theme={"light"}
//                               defaultSelectedKeys={pathname}
//                               selectedKeys={pathname}
//                               style={{
//                                   // height: '100%',
//                                   width: "48vw",
//                                   borderBottom: 0,
//                                   backgroundColor: 'transparent',
//                                   display: "flex",
//                                   justifyContent: "flex-end"
//                               }}
//                             // inlineCollapsed={true}
//                         >
//                             <Menu.Item key="/">
//                                 {/*<div>首页</div>*/}
//                                 <Link to='/' className={s("menu-item")}>首页</Link>
//                             </Menu.Item>
//                             {
//                                 token &&
//                                 <>
//                                     <Menu.Item key="/quantify">
//                                         <Link to='/quantify' className={s("menu-item")}>量化交易</Link>
//                                     </Menu.Item>
//                                     <Menu.Item key="/extraction">
//                                         <Link to='/extraction' className={s("menu-item")}>信息抽取</Link>
//                                     </Menu.Item>
//                                 </>
//                             }
//                             <Menu.Item key="/introduce">
//                                 <Link to='/introduce' className={s("menu-item")}>平台介绍</Link>
//                             </Menu.Item>
//                             <Menu.Item key="/about">
//                                 <Link to='/about' className={s("menu-item")}>关于我们</Link>
//                             </Menu.Item>
//                         </Menu>
//                         <div className={s("login-button-box")}>
//                             {
//                                 !token
//                                     ?
//                                     <Link to={'/login'} className={s("login-button")}>登录</Link>
//                                     :
//                                     <div className={s("avar-box")}>
//                                         <img src={require("../../assert/avar.png")}/>
//                                     </div>
//                             }
//                         </div>
//                     </div>
//                 </div>
//             </Header>
//         </div>
//       );
// }
// function NewEmpty() {
//     return (
//         <div className={s("GreyEmpty")}>
//         </div>
//     )
// }

function Introduce() {
    const [currentOption, setCurrentOption] = useState('Introduction');

    function handleOptionChange(option) {
        setCurrentOption(option);
    }

    return (
        <div className={s("introduce")}>
            {/*<NewHeader/>*/}

            <NewSidebar onOptionChange={handleOptionChange}/>
            {/*<NewEmpty/>*/}
            <NewContent currentOption={currentOption}/>

        </div>
    );
}

export default Introduce
