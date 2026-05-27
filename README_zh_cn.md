# SimpleBuildingSimulation

一个基于 Reflex 搭建的网页端应用程序，用于建筑设备服务模拟与室内热舒适度分析。

---

## 1. 环境准备与安装

本指南将协助您配置本地开发环境。开始前，请确保您的系统已安装 **Python 3.8+** 并已将其配置到系统的环境变量（PATH）中。

### 1.1 准备工作与虚拟环境配置

为避免依赖项冲突，强烈建议将该项目部署在独立的虚拟环境（`virtualenv`）中。

#### 步骤 1：安装 virtualenv 工具
在当前 Python 解释器中运行以下命令，使用包管理器安装 `virtualenv` 工具：
```bash
python -m pip install virtualenv
```

#### 步骤 2：创建虚拟环境

创建一个独立的虚拟环境。您可以指定任意本地路径，但通常的做法是在项目根目录或用户目录下创建一个名为 `.venv` 的文件夹。这里以创建名为 `venv1025` 的环境为例：

```bash
# 在用户目录下创建指定名称的虚拟环境示例

python -m virtualenv "C:\Users\<your_username>\venv1025"
```

> **提示：** 请将 `<your_username>` 替换为您实际的 Windows 系统账户名称。

#### 步骤 3：激活虚拟环境（Windows PowerShell）

在执行激活脚本之前，PowerShell 可能会因为系统安全策略限制脚本运行。请先执行以下命令修改执行策略：

```powershell
# 为当前用户修改脚本执行策略

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

当系统弹出确认提示时，输入 `Y` 并按下 **回车键（Enter）** 确认。

随后，进入对应的目录并激活该虚拟环境：

```powershell
1. cd "C:\Users\<your_username>"

2. .\venv1025\Scripts\activate
```

**验证标志：** 激活成功后，您的终端提示符最前端会出现 `(venv1025)` 字样。

---

### 1.2 安装 Reflex

在激活的虚拟环境中，使用 `pip` 安装 **Reflex v0.6.7**。针对中国大陆地区的开发者，建议使用清华大学 TUNA 镜像源以加速下载：

```bash
pip install reflex==0.6.7 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 2. 项目获取与部署

您可以通过以下两种方法之一获取最新的项目源代码。

### 2.1 获取源代码

#### 选项 A：通过 Git 克隆（推荐）

如果您的系统中已安装 Git，可以直接将仓库克隆到本地工作区：

```bash
# 进入您的工作区目录（例如：C:\Users\<your_username>\EcoSim_Simple_Building_Simulation）

cd "C:\Users\<your_username>\EcoSim_Simple_Building_Simulation"

# 克隆远程仓库

git clone [https://github.com/Yorking6/EcoSim_Simple_Building_Simulation.git](https://github.com/Yorking6/EcoSim_Simple_Building_Simulation.git)

# 进入项目根目录

cd SimpleBuildingSimulation
```

#### 选项 B：手动下载

1. 访问 GitHub 上的项目仓库页面。
2. 点击绿色的 **Code** 按钮并选择 **Download ZIP**。
3. 将下载的 ZIP 压缩包解压到指定文件夹，例如：
> `C:\Users\<your_username>\EcoSim_Simple_Building_Simulation`


4. 打开 PowerShell 并通过 `cd` 命令进入该文件夹：
```bash
cd "C:\Users\<your_username>\EcoSim_Simple_Building_Simulation"
```


---

### 2.2 初始化项目依赖

进入项目根目录后，需要触发 Reflex 的内部安装机制。与初始化一个空白项目不同，在此处运行初始化命令时，Reflex 会自动检测现有的 `rxconfig.py` 配置文件，并安装运行本模拟应用所需的 Web 环境（Node.js/npm）：

```bash
# 确保在运行此命令前，您的虚拟环境 (venv1025) 已处于激活状态

reflex init --loglevel debug
```

**关于后台任务的注意事项：**
Reflex 会自动在后台配置一个独立的轻量化前端环境。此过程需要下载数百兆的依赖包。根据您的网络状况，这可能需要 **10–20 分钟**。请耐心等待其完全结束，在此期间请勿中断程序。

---

## 3. 运行应用程序

环境配置完成后，即可启动应用程序并开始进行建筑能耗模拟。

### 3.1 启动开发服务器

在项目根目录下运行以下命令（**请确保此时虚拟环境仍处于激活状态**）：

```bash
reflex run --loglevel debug

```

---

### 3.2 访问网页端应用

当前端编译与依赖打包流程结束后，终端将会输出前端用户界面（UI）和后端服务器的具体运行本地地址。

* **默认前端 URL：** 通常为 `http://localhost:3000` 或 `http://localhost:3001`
* **访问方式：** 打开浏览器，直接输入终端输出中显示的实际 URL 即可。

---

## 4. 网页端应用使用说明

当本地服务器成功运行且您已在浏览器中打开 `http://localhost:3000` 后，您将看到 **EcoSim Pro** 的操作界面。这是一个专为建筑能耗模拟工作流打造的专业图形化（GUI）控制面板。

该应用会将用户在前端输入的各项参数，自动转化为底层 EnergyPlus 模型文件（IDF）的修改指令，在后台调用热工计算引擎，并将结构化的分析结果实时渲染并反馈至前端。

---

### 4.1 界面结构与页面导航

本系统采用了符合工程实践逻辑的、以工作流为导向的多页面导航架构，完美契合了建筑结构设计与负荷规划的各个阶段：

* **Home（首页）：** 系统的欢迎与入口页面，提供了软件运行核心目标与整体框架的概述。
* **Geometry Setting（几何设置）：** 专用视图，用于控制、修改外窗尺寸的空间物理参数和边界定义。
* **Material Setting（材料设置）：** 围护结构配置页面，用于为建筑的不同结构组件分配特定的材料矩阵和热工参数。
* **Residential Setting（居住设置）：** 区域运行剖面控制台，用于配置人员密度、内部发热阵列以及长期的运行时间表（Schedules）。
* **About（关于）：** 技术背景页面，展示了系统的构建参数、后端技术栈架构以及开发者的相关信息。

---

### 4.2 模拟操作指南

#### 功能 A：修改外窗几何尺寸

1. 通过主导航栏切换至 **Geometry Setting（几何设置）** 工作区。
2. 聚焦于几何属性选择器下拉菜单，选择您想要调整的几何变换特征是窗户的 **Length（长度）** 还是 **Height（高度）**。
3. 在数值输入框中键入合法的浮点数（例如输入 `3.0`，代表将对应的边界尺寸设定为 3.0 米）。
4. 点击 **Start to simulation!（开始模拟！）** 按钮。系统将自动改写底层区域的顶点坐标，重新初始化基准 `1ZoneIdealSys.idf` 模型矩阵，调用后台计算引擎，并刷新前端的能耗数据块。

#### 功能 B：材料构造与热工性能自定义

1. 将鼠标光标引导至 **Material Setting（材料设置）** 路由页面。
2. 展开 **Window Material Type（外窗材料类型）** 下拉矩阵，选择目标装配层（选项涵盖了从传统的基准 **Double Pane Window（双层玻璃窗）** 到高热工性能的低辐射 **Double Pane Low-E Window（双层低辐射玻璃窗）** 构造）。
3. 通过 **Wall Material Type（墙体材料类型）** 配置下拉菜单更新外墙的结构边界（选项将常规的 **Common Brick Wall（普通砖墙）** 建筑组件与高热阻的 **High-Efficiency Insulated Wall（高效保温墙）** 系统进行了映射）。
4. 点击 **Start to simulation!（开始模拟！）** 启动模拟线程，用以定性与定量地评估不同的传热系数（U值）和太阳得热系数（SHGC）对建筑年累计基础负荷的影响。

#### 功能 C：微调内部热负荷与运行时间表

1. 切换至 **Residential Setting（居住设置）** 控制面板。
2. 定位到内部时间表矩阵下拉菜单，并选择对应项（例如 `OCCUPY-1`），以声明该热工区域内人员高频活动的实际时间段。
3. 在 **Number of people（人数）** 参数输入框中键入严格的整数（例如输入 `5` 代表该区域内存在 5 个标准人员单位）。
4. 点击 **Start to simulation!（开始模拟！）**。应用程序会将该整数块传递给后台，用以精确计算人员散发的人体显热与潜热负荷，并结合本地气象数据集（`shanghai_2017.epw`）重新评估该区域的热力学逐时动态负荷趋势。

---

### 4.3 结果读取与数据分析

在触发模拟后，前端状态栏会临时显示提示字符串：`"Simulation in progress. Please wait a moment…"`（模拟运行中，请稍候……）。当后台计算线程正常退出后，本地客户端的状态管理器将使用 Pandas 对原始数据块进行结构化清洗，并将处理后的指标同步输送到前端的两个核心分析模块中：

1. **数值统计区块（Numerical Metrics Blocks）：** 一个直观的绝对能耗追踪摘要面板，将计算得出的 HVAC 累计运行负荷直接以具体的年能耗量数字（单位：千瓦时/年，**kWh/year**）展现。
2. **集成 Recharts 柱状图（Integrated Recharts Bar Chart）：** 一个自动响应式的动态分析图表画布，同屏并列对比展示年累计 **Cooling Energy（供冷能耗）** 与 **Heating Energy（供热能耗）**。该图表使您能够快速评估围护结构或人员扰动带来的热工性能改变，并在多次不同的实验迭代之间轻松进行交叉对比。