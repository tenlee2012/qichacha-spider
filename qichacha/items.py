# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re


uid_reg = re.compile(r'\S*firm_(\S*).html')


class CompanyBaseInfo(scrapy.Item):
    """
    公司基本信息
    """
    uid = scrapy.Field()  # 在企查查中的唯一ID
    name = scrapy.Field()  # 公司名称
    image = scrapy.Field()  # 公司图标
    phone = scrapy.Field()  # 联系电话
    email = scrapy.Field()  # 邮箱
    official_website = scrapy.Field()  # 官网
    address = scrapy.Field()  # 地址
    legal_person = scrapy.Field()  # 法人
    person_url = scrapy.Field()  # 法人url
    registered_capital = scrapy.Field()  # 注册资本
    paid_in_capital = scrapy.Field()  # 实缴资本
    continual_situation = scrapy.Field()  # 经营状态
    found_date = scrapy.Field()  # 成立日期
    reg_number = scrapy.Field()  # 注册号
    org_code = scrapy.Field()  # 组织机构代码
    tax_number = scrapy.Field()  # 纳税人识别号
    social_credit_code = scrapy.Field()  # 统一社会信用代码
    type = scrapy.Field()  # 公司类型
    industry = scrapy.Field()  # 所属行业
    approval_date = scrapy.Field()  # 核准日期
    register_office = scrapy.Field()  # 登记机关
    area = scrapy.Field()  # 所处地区
    en_name = scrapy.Field()  # 英文名称
    used_name = scrapy.Field()  # 曾用名
    operation_mode = scrapy.Field()  # 经营方式
    workforce = scrapy.Field()  # 人员规模
    business_term = scrapy.Field()  # 营业期限
    business_scope = scrapy.Field()  # 经营范围

    source_url = scrapy.Field()  # 来源url

    @staticmethod
    def convert_value(value):
        if isinstance(value, str):
            value = str(value).strip()
            if value == '-':
                return None
            if value == '暂无':
                return None
            return value
        elif isinstance(value, list):
            return [v.strip() for v in value]

    def __setitem__(self, key, value):
        if key in self.fields:
            value = self.convert_value(value)
            self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                           (self.__class__.__name__, key))


def parse_response(response):
    company = CompanyBaseInfo()
    company['uid'] = uid_reg.findall(response.url)[0]
    company['source_url'] = response.url

    company['name'] = response.css('.row.title > h1::text').extract_first()
    company['image'] = response.xpath('//*[@id="company-top"]/div/div[1]/div/img/@src').extract_first()
    company['phone'] = response.xpath('//*[@id="company-top"]/div/div[2]/div[2]/span[2]/span/text()').extract_first()
    company['email'] = response.xpath('//*[@id="company-top"]/div/div[2]/div[3]/span[2]/a/text()').extract_first()
    company['official_website'] = response.xpath(
        '//*[@id="company-top"]/div/div[2]/div[3]/span[4]/text()').extract_first()
    company['address'] = response.xpath('//*[@id="company-top"]/div/div[2]/div[4]/span[2]/a[1]/text()').extract_first()
    company['legal_person'] = response.xpath(
        '//*[@id="Cominfo"]/table[1]/tr[2]/td[1]/div/div[1]/div[2]/a[1]/text()').extract_first()
    company['person_url'] = response.xpath(
        '//*[@id="Cominfo"]/table[1]/tr[2]/td[1]/div/div[1]/div[2]/a[1]/@href').extract_first()

    # normalize-space()作用是去掉td 中 a 的text值
    infos = response.xpath("//*[@id='Cominfo']/table[2]/tr/td[(@class='')]/text()[normalize-space()]").extract()
    if len(infos) != 19 and len(infos) != 20:
        with open(response.url.replace('/', '-'), 'w') as f:
            f.write(response.text)
        raise ValueError("url:{}, 解析错误".format(response.url))
    company['registered_capital'] = infos[0]
    company['paid_in_capital'] = infos[1]
    company['continual_situation'] = infos[2]
    company['found_date'] = infos[3]
    company['reg_number'] = infos[4]
    company['org_code'] = infos[5]
    company['tax_number'] = infos[6]
    company['social_credit_code'] = infos[7]
    company['type'] = infos[8]
    company['industry'] = infos[9]
    company['approval_date'] = infos[10]
    company['register_office'] = infos[11]
    company['area'] = infos[12]
    company['en_name'] = infos[13]

    if len(infos) == 20:
        company['used_name'] = infos[14]
    else:
        company['used_name'] = response.xpath('//*[@id="Cominfo"]/table[2]/tr[8]/td[2]/span/text()').extract_first()

    company['operation_mode'] = infos[-5]
    company['workforce'] = infos[-4]
    company['business_term'] = infos[-3]
    company['business_scope'] = infos[-1]
    return company
