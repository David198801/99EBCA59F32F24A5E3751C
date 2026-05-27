
gateway_urls = []
file_urls = []
output_lines = []
output_lines += [
"[color=#0000ff][size=6][b]PikPak[/b][/size][/color]",
"\n\n",
"[color=#0000ff][size=6][b]IPFS[/b][/size][/color]",
"选择以下节点其中一个进行下载，或者在[url=https://crust.subsquare.io/treasury/proposals]subsquare[/url]寻找可用节点替换域名下载。",
"\n\n"
]

#文件链接固定前缀
prefix = "https://ipfs.io/"

special_gateway = [('节点0(ipfs自动测速)','https://ipfs-checker.1kbtool.com/')]

with open("crust_gateway.txt","r",encoding='utf8') as txt:
    gateway_urls = [x.replace('\n','') for x in txt.readlines() if x]
    
with open("crust_files.txt","r",encoding='utf8') as txt:
    file_urls = [x.replace('\n','') for x in txt.readlines() if x]
    
for g in special_gateway:
    g_name = g[0]
    g_url = g[1]
    
    #标题
    output_lines.append(f"[size=3][b]{g_name}[/b][/size]")
    #url
    for f in file_urls:
        url = f.replace(prefix+"ipfs/",(g_url if g_url.endswith('/') else g_url+"/" ))
        output_lines.append(f"[url]{url}[/url]")
        
    output_lines.append("\n")
    
    
for g in gateway_urls:
    sp = g.split(",")
    g_name = sp[0]
    g_url = sp[1]
    
    #标题
    output_lines.append(f"[size=3][b]{g_name}[/b][/size]")
    #url
    for f in file_urls:
        url = f.replace(prefix,(g_url if g_url.endswith('/') else g_url+"/" ))
        output_lines.append(f"[url]{url}[/url]")
        
    output_lines.append("\n")

with open("crust_output.txt","w",encoding='utf8') as txt:
    for i in output_lines:
        txt.write(i+"\n")