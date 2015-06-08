### 交互语义规则定义

service := statements [connect_statement statements] [time_condition]
statements := operate object 

object := [number_ad] [dealer_conditon] [component_condition] [extra_conditon] object_vocabulary
number_ad := <数量副词>
dealer_condition := <商家限制>
component_condition := <材料限制>
extra_condition := <其他附赠限制>
object_vocabulary := <描述的商品词汇>
connect_statement := <链接语句>
time_condition := <时间限制>

// service 是一个完整的服务。如给我来一份比较简单的套餐，最好十分钟送到;来一包烟和一瓶王老吉
// statements 为最基本的完整操作行为，如买包烟，来一份大肉水饺等;

### 语义行为分析
底层在处理语句中operate时抽取的基本接口有: 查询(select)，再筛选，最优组合配对(resort)

select WITH [number_ad,][component_condition,][extra_condition,]object_statement

filter WITH [dealer_condition,][time_condition]

resort WITH [seam_dealer]

### 实现接口定义
select(object, number=1, com_cond=None, extra_cond=None)
filter(dealer=None, time_cond=60)
resort(strategy='seam_dealer')
