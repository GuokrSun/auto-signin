# Action 使用指南

## 准备工作

1. 创建一个新的公开仓库, 如 `aliyun-signin-action`
   > 推荐使用公开仓库, 按照 GitHub [计费说明](https://github.com/settings/billing/plans), 公开仓库的 Actions 不计入使用时间
   > 不需要 Fork 本仓库, 采用 `uses` 的方式引用本仓库 Action, 实现自动更新*

2. 在仓库中新建文件 `.github/workflows/signin.yml`
   > 用于配置 Github Action 的工作流

## 编写 Action 配置

1. 创建 `.github/workflows/signin.yml` 文件, 写入 Action 配置, 以下是参考配置
    ```yaml
    name: signin

    on:
      workflow_dispatch:
      schedule:
        # UTC 1点30分(北京时间 9点30分)
        - cron: 30 1 * * *

    jobs:
      signin:
        name: signin
        runs-on: ubuntu-latest
        steps:
          - uses: GuokrSun/auto-signin@master
            with:
                TIEBA_BDUSS: ${{ secrets.TIEBA_BDUSS }}
                GLADOS_COOKIE: ${{ secrets.GLADOS_COOKIE }}
                FULIBA_COOKIE: ${{ secrets.FULIBA_COOKIE }}
                FULIBA_USERNAME: ${{ secrets.FULIBA_USERNAME }}
                PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
                PUSHPLUS_TOPIC: ${{ secrets.PUSHPLUS_TOPIC }}
    ```
2. 按需修改 `corn` 定时运行时间, 推荐在中国时间 22:00 之后.

## 配置 GitHub Secrets

在仓库的 `Settings` -> `Secrets and Variables` -> `Actions` 中点击 `New repository secret` 按照推送需要添加 Secrets.
添加时 `Name` 为下方全大写的配置 key, `Secret` 为对应的值, 均不需要引号.

- `TIEBA_BDUSS`    [推荐] 百度贴吧 cookie-BDUSS
- `FULIBA_COOKIE`  [推荐] 福利吧 cookie
- `FULIBA_USERNAME`[推荐] 福利吧 username
- `PUSHPLUS_TOKEN` [可选] *PushPlus Token*
- `PUSHPLUS_TOPIC` [可选] *PushPlus 群组编码，不填仅发送给自己*

正确添加后应显示在 `Repository secrets` 区域而非 `Environment secrets`.

[PushPlus 官方文档](https://www.pushplus.plus)

## 运行 Action

你将有两种方式运行 Action

- 手动运行
    - 在仓库的 `Actions` -> `Signin` -> `Run workflow` 中点击 `Run workflow` 按钮运行
- 定时自动运行
    - 上方参考的配置文件中已经配置了定时自动运行, 每天国际时间 17:20 运行一次, 中国时间 01:20, 可根据需要调整

## 查看结果

可以在运行的 Action 运行记录中的 `Run GuokrSun/auto-signin@master` 末尾查看运行结果

## 鸣谢
代码仓库
- [百度贴吧](https://github.com/gwtak/TieBaSign)
- [福利吧](https://gitee.com/L_lawliet0309/fuliba_SCF)
- [glados机场](https://github.com/lukesyy/glados_automation)
