# cl-cli
CodingHub命令行工具(Command line tool for codinghub-cloud)

https://github.com/zuiwan

## 1. 安装(Install)

```
python setup.py install
```


## 2. 登陆(Login)

```
cl login
```


## 3. 管理项目
### 3.1 初始化项目(Init)

```
cl init --id <project_id>
```
or
```
cl init --name <project_name>
```

### 3.2 运行项目(Run)

```
cl run <command>
```


### 3.3 输出日志(Logs)

```
cl logs <run_id>
```

### 3.4 输出结果(Output)

```
cl output <run_id>
```

## 4. 管理数据集
数据集也可以用作个人的云盘。

### 4.1 初始化数据集
```
cl data init --id <dataset_id>
```
or
```
cl data init --name <dataset_name>
```

### 4.2 上传数据集
```
cl data upload
```

### 4.3 查看数据集状态
```
cl data status [dataset_id]
```

### 4.4 浏览数据集
```
cl data output
```


## 5. 管理博客

### 5.1 初始化
```
cl blog init [OPTIONS] [ARGS]
```
Options：

|选项|默认|描述|
|---|---|---|
|--project||该文件夹下所有博客均绑定项目|

### 5.2 创建博客文章
```
cl blog new <blog_title>
```
Options：

|选项|默认|描述|
|---|---|---|
|--category, -c||分类|
|--tag, -t||标签|
|--project, -p||绑定项目|
|--private|False|是否公开|

### 5.3 本地提交博客
```
cl blog commit [OPTIONS]
```
Options：

|选项|默认|描述|
|---|---|---|
|--message, -m||提交记录|

### 5.4 发布本地提交
```
cl blog publish
```


## 6. 管理收藏
### 6.1 添加收藏
```
cl fav add [OPTIONS] [ARGS]
```

示例：
1. 添加单个url
```
cl fav add --url <url>
```
2. 从文本文件批量添加url
```
cl fav add --url -r <url.txt>
```

Options：

|选项|默认|描述|
|---|---|---|
|--url||类型，URL收藏|
|--detail|False|为True时，服务器将爬取URL中的网页内容|
|--tag, -t||标签|
|--message， -m||描述|
|--project, -p||绑定项目|
|--blog, -b||绑定博客|

### 6.2 搜索收藏
```
cl fav search <key_words>
```


## TODO
1. 支持更多收藏类型
