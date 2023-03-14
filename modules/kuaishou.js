exports.id='kuaishou'
exports.name='kuaishou'
exports.host='https://tutjiexi.com/parse/tutu'
exports.headers= { 
	"accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,ru;q=0.8",
    "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-datadog-origin": "rum",
    "x-datadog-parent-id": "3159239160947590253",
    "x-datadog-sampled": "1",
    "x-datadog-sampling-priority": "1",
    "x-datadog-trace-id": "8371949252371235631",
    "cookie":"__yjs_duid=1_310c22c85e9c3aed325c291885a3a7fe1678762990563; tokens=222e787d612523652c513017d744a4de",
    "Referer": "https://tutjiexi.com",
    "Referrer-Policy": "strict-origin-when-cross-origin",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

exports.install= async function(){

}

exports.toFile=async function(url,fname){
	var res=await this.parse(url)
	if(res.status===200){
		var name=fname?fname:(UID()+'.mp4')
		var path=await XGETFILE(res.data.sourceUrl,name)
		return {path:path,name:name}
	}else{
		return new Error(res.msg)
	}
}

exports.parse=async function(url){
	var opt={
		url:this.host,
		method:'POST',
		headers:this.headers
	}
	opt.body=JSON.stringify({
	  "pageUrl": url,
	  "flatformCode": "KUAISHOU",
	  "tt": new Date().getTime(),
	  "ss": "NmZmOGFjNmI0NTZlMmVhZjdmYmRmMWMyNDNjOTNiMGE=",
	  "t": new Date().getTime(),
	  "s": "od3f0kzeza4lod4m0krdytgjzqohon3c0q0m0dwmndwa"
	})
	return await XAPI(opt)
}
exports.download=async function(url){

}

async function XGETFILE(url,name){
	var a=['videos']
	PATH.mkdir(PATH.public(a.join('/')));
	if(name)a.push(name)
	var path=PATH.public(a.join('/'))
	console.log(path)
	return new Promise(function (resolve, reject) {
		DOWNLOAD(url, path,()=>{
			resolve(a.join('/'))
		}, 300000);
	})
	
}

function XAPI(opt,type){
	opt=opt||{};
	opt.timeout=300000;
	return new Promise(function (resolve, reject) {
		opt.callback=function(err,res){
			if(err||res.status!==200){
				return reject(err);
			}
			try{
				var body=JSON.parse(res.body);
			}catch(err){
				var body=res.body;
			}
			return resolve(body);
		}
		REQUEST(opt);
	})
}