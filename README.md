# Networks_Rules

[![GitHub Stars](https://img.shields.io/github/stars/hanilbert/Networks_Rules?style=social)](https://github.com/hanilbert/Networks_Rules/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/hanilbert/Networks_Rules?style=social)](https://github.com/hanilbert/Networks_Rules/network/members)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/hanilbert/Networks_Rules)](https://github.com/hanilbert/Networks_Rules/commits)
[![GitHub License](https://img.shields.io/github/license/hanilbert/Networks_Rules)](https://github.com/hanilbert/Networks_Rules/blob/main/LICENSE)

这个仓库用于存储个人使用的网络代理规则配置，包括 Clash、Surge 等工具的分流规则。

## 项目说明

本项目主要包含：
- Clash 规则配置
- Surge 规则配置
- 自定义分流规则

## 目录结构

```
.
└── rules/          # 规则文件目录
    ├── clash/      # Clash 规则配置
    │   ├── exness.yaml
    │   ├── icmarkets.yaml
    │   ├── thinkmarkets.yaml
    │   ├── easymarkets.yaml
    │   └── trading_platform.yaml    # 合并规则
    └── surge/      # Surge 规则配置
        ├── exness.list
        ├── icmarkets.list
        ├── thinkmarkets.list
        ├── easymarkets.list
        └── trading_platform.list    # 合并规则
```

## 规则列表

### 交易平台规则
- Exness
- IC Markets
- ThinkMarkets
- EasyMarkets

### 合并规则
- Trading Platform（包含所有交易平台规则）

## 使用说明

1. 规则文件可以直接导入到相应的客户端使用
2. 建议定期更新规则以保持最佳使用体验
3. 部分规则可能需要根据个人需求进行自定义调整
4. 可以选择使用单独的规则文件或合并规则文件

## 注意事项

- 本仓库仅用于个人使用
- 请遵守相关法律法规
- 建议定期备份您的规则配置
