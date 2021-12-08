import re

# 预警标题清洗
titleRules = [
    '([【\[涉].*)\n',
]

# 预警内容清洗
contentRules = [
    '\n(.*?[。姓名]。)',
    '今日无新增'
]


# 预警标签清洗
labelRules = [
    '[\[【](.*?)[\]】]',
]
