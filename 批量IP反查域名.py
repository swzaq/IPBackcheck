import re, time, requests,os
#守卫者安全 批量通过ip反查域名脚本

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36' #火狐浏览器user-agent,后期添加随机功能

# ip138
headers_ip138 = {
    'Host': 'site.ip138.com',
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://site.ip138.com/'}
# 爱站
headers_aizhan = {
    'Host': 'dns.aizhan.com',
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dns.aizhan.com/'}


def ip138_spider(ip):
    ip138_url = 'https://site.ip138.com/' + str(ip) + '/'
    ip138_r = requests.get(url=ip138_url, headers=headers_ip138, timeout=3).text
    ip138_address = re.findall(r"<h3>(.*?)</h3>", ip138_r)   # 归属地
    result=['[+]ip138平台下'+ip+'反查结果信息如下：']
    all=''
    if '<li>暂无结果</li>' in ip138_r:
        result.append('归属地：'+ip138_address[0]+'未查到相关绑定信息！')
    else:
        result_time = re.findall(r"""class="date">(.*?)</span>""", ip138_r)  # 绑定域名时间
        result_site = re.findall(r"""</span><a href="/(.*?)/" target="_blank">""", ip138_r)  # 绑定域名结果
        result.append('归属地：'+ip138_address[0])
        
        result.append('该IP一共解析了'+str(len(result_site))+'个域名！')
        for i, j in enumerate(result_time):
          
            all=str(j)+':   '+result_site[i]
            result.append(all)

    with open("IP反查结果.txt", 'a') as f: 
        for i in result:
            f.write(i + "\n") 
        f.write('\n')
        f.close()
    

def aizhan_spider(ip):
    result=['[+]爱站平台下'+ip+'反查结果信息如下：']
    aizhan_url = 'https://dns.aizhan.com/' + str(ip) + '/'
    aizhan_r = requests.get(url=aizhan_url, headers=headers_aizhan, timeout=2).text
    aizhan_address = re.findall(r'''<strong>(.*?)</strong>''',  aizhan_r)# 归属地
    aizhan_nums = re.findall(r'''<span class="red">(.*?)</span>''', aizhan_r)#该ip解析过多少个域名
    result.append('该ip一共解析了：'+aizhan_nums[0]+'个域名！')
    result.append('归属地：'+aizhan_address[0])
    if int(aizhan_nums[0]) > 0:
        if int(aizhan_nums[0]) > 20:
            # 计算多少页
            pages = (int(aizhan_nums[0]) % 20) + (int(aizhan_nums[0]) // 20)
            for page in range(1, pages+1):
                aizhan_page_url = aizhan_url + str(page) + '/'
                aizhan_page_r = requests.get(url=aizhan_page_url, headers=headers_aizhan, timeout=2).text               
                aizhan_domains = re.findall(r'''rel="nofollow" target="_blank">(.*?)</a>''', aizhan_page_r)
                for aizhan_domain in aizhan_domains:
                    result.append(aizhan_domain)# 取出该ip曾经解析过的域名    
                time.sleep(0.5)
        else:
            
            aizhan_domains = re.findall(r'''rel="nofollow" target="_blank">(.*?)</a>''', aizhan_r)
            for aizhan_domain in aizhan_domains:
                result.append(aizhan_domain)
    else:
        result.append('共有0个域名解析到该IP')
        
    with open("IP反查结果.txt", 'a') as f: 
        for i in result:
            f.write(i + "\n") 
        f.write('\n')
        f.close()


if __name__ == '__main__':
    if os.path.exists("IP反查结果.txt"): 
        f = open("IP反查结果.txt", 'w') 
        f.truncate() 
    
    IP=''
    IP_lists = open("IP列表.txt", 'r').readlines()
    
    for i in IP_lists:
        i=i.strip('\n')
        IP=i
        ip138_spider(IP)
        time.sleep(1)
        aizhan_spider(IP)
        
        
    print('IP反查完成！')

