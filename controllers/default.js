
const kuaishou=MODULE('kuaishou');
const sms=MODULE('sms');
exports.install = function() {

	ROUTE('/');
	ROUTE('/parse/', view_parse);

};

async function view_parse() {
	var self = this;
	var url=this.query.url||''
	if(url){
		U.queue('aaa',10,async function(next){
			var id=UID();
			var name=id+'.mp4'
			var res=await kuaishou.toFile(url,name)
			var response = await SHELL('python video.py '+res.name);
        	var url=`${ self.uri.protocol }//${ self.uri.hostname }/videos/${ id }_cartoon_audio.mp4`;
			sms.send('【视频转换】成功：'+url)
			next()
		})
		return this.json({code:200,data:res})
	}else{
		return this.json({code:400,msg:'请输入url'})
	}
}