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
    name: Aliyun Signin

    on:
      schedule:
       # 每天国际时间 14:40 运行一次, 中国时间 22:40
        - cron: '40 14 * * *'
      workflow_dispatch:
    jobs:
      signin:
        name: Aliyun Signin
        runs-on: ubuntu-latest
        steps:
          - uses: ImYrS/aliyun-auto-signin@main
            with:
              REFRESH_TOKENS: ${{ secrets.REFRESH_TOKENS }}
              GP_TOKEN: ${{ secrets.GP_TOKEN}}
              PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
              PUSHPLUS_TOPIC: ${{ secrets.PUSHPLUS_TOPIC }}
    ```

2. 按需修改 `corn` 定时运行时间, 推荐在中国时间 22:00 之后.

## 配置 GitHub Secrets

在仓库的 `Settings` -> `Secrets and Variables` -> `Actions` 中点击 `New repository secret` 按照推送需要添加 Secrets.
添加时 `Name` 为下方全大写的配置 key, `Secret` 为对应的值, 均不需要引号.

- `REFRESH_TOKENS` **[必选]** *阿里云盘 refresh token, 多账户使用英文逗号 (,) 分隔*
- `GP_TOKEN` [推荐] 在 Action 中运行时更新 refresh token
- `PUSHPLUS_TOKEN` [可选] *PushPlus Token*
- `PUSHPLUS_TOPIC` [可选] *PushPlus 群组编码，不填仅发送给自己*

[PushPlus 官方文档](https://www.pushplus.plus)

> **获取 GP_TOKEN 的方法**
>
> 点击 GitHub 头像 -> `Settings` (注意与配置 Secrets 不是同一个
> Settings) -> `Developer settings` -> `Personal access token` -> `Tokens(classic)` -> `Generate new token`
>
> 权限选择 `repo`, 不然不能更新 Secrets. 记住生成的 token, 离开页面后无法查看
> 这些 `Secrets` 将加密存储在 GitHub, 无法被直接读取, 但可以在 Action 中使用

正确添加后应显示在 `Repository secrets` 区域而非 `Environment secrets`.

## 运行 Action

你将有两种方式运行 Action

- 手动运行
    - 在仓库的 `Actions` -> `Aliyun Signin` -> `Run workflow` 中点击 `Run workflow` 按钮运行
- 定时自动运行
    - 上方参考的配置文件中已经配置了定时自动运行, 每天国际时间 17:20 运行一次, 中国时间 01:20, 可根据需要调整

## 查看结果

可以在运行的 Action 运行记录中的 `Run ImYrS/aliyun-auto-signin@main` 末尾查看运行结果
