# super-spoon
基于青龙面板实现

## 使用方法
- 方法一：进入青龙面板容器，运行命令： `ql repo https://ghproxy.com/https://github.com/scoful/super-spoon.git`
- 方法二：在青龙面板首页右上角，添加任务，名称和定时规则随便输入，命令填：`ql repo https://ghproxy.com/https://github.com/scoful/super-spoon.git` ，成功后再删了任务


## 支持的脚本说明

- idena，检测是否掉线，环境变量：`IDENA_ACCOUNT`，idena账号，用&分隔
- 青云，自动签到，环境变量：`QINGCLOUD_COOKIE`，手动签到一次，查找接口`https://points.qingcloud.com/api/scorecheckin/checkin?变量内容` ，浏览器开发者模式获取变量内容
- 什么值得买，自动签到，环境变量：`SMZDM_COOKIE`，手动签到一次，浏览器开发者模式复制整个cookie