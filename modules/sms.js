exports.name="sms"
exports.url= 'https://open.feishu.cn/open-apis/bot/v2/hook/1e097f61-0ecc-4718-8752-de0dc3c38b11'//"https://sms.yunpian.com/v2/sms/single_send.json"

exports.install=async function(){
	//this.send('adad')
}



exports.send=async function(message,type){
	var opt={
		url:this.url,
		method:"post",
		type:'json',
		body:JSON.stringify(type?message:{
			"msg_type":"text",
			"content":{
				"text":CONF.server_name+' '+message
			}
		})
	}
	return await promiseRequest(opt)
}

function promiseRequest(opt){
		opt=opt||{};
		return new Promise(function (resolve, reject) {
			
			opt.callback=function(err,res){
				console.log(res.body)
				if(err||res.status!==200)return reject();
				try{
					var body= JSON.parse(res.body);
				}catch(err){
					var body=res.body;
				}
				return resolve(body);
			}
			REQUEST(opt);
		});
	}

exports.Request =  promiseRequest