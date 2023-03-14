
const kuaishou=MODULE('kuaishou');
exports.install = function() {

	ROUTE('/');
	ROUTE('/parse/', view_parse);

};

async function view_parse() {
	var self = this;
	var url=this.query.url||''
	if(url){
		var res=await kuaishou.toFile(url)
		U.queue('aaa',10,async function(next){
			var response = await SHELL('python video.py '+res.name);
			console.log(response)
			next()
		})
		return this.json({code:200,data:res})
	}else{
		return this.json({code:400,msg:'请输入url'})
	}
}