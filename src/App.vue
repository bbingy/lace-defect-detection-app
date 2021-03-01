<template>
  <div id="app" class="home">
    <el-container style="height:100%;width:100%">
      <el-header>花边布缺陷检测系统
        <el-select v-model="value" filterable style="float:right; width:122px" placeholder="破洞" @change="selectVideo" class="select-style" popper-class="select-option">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <span style="float:right; margin-right:10px; font-size:18px">视频选择:  </span>
      </el-header>
      <el-main>
        <!-- <p style="margin-up:10;line-height:0;color:#FFFFFF;">出现缺陷的时间点: 0s</p> -->
        <div class="upleft">
          <video-player  class="video-player vjs-custom-skin"
                          ref="videoPlayer" 
                          :playsinline="true" 
                          :options="playerOptions"
                          @pause="detectDefect($event)">
          </video-player>
        </div>
        <div class="upright">
          <h2 style="line-height:30px">系统简介</h2>
          <p style="line-height:30px" align="left">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本系统基于机器视觉原理检测织物表面缺陷，能够实现自动对花边布视频中疵点的检测，并以二值化图像的形式显示出缺陷位置。</p>
        </div>
        <!-- <div class="left">
          <el-upload
            class="avatar-uploader"
            action="http://166.111.180.117:8000/upload"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img  v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-if="uploadFlag=='False'" class="el-icon-upload"></i>
            <div v-if="uploadFlag=='False'" class="el-upload__text"><em>click to upload your photo</em></div>
          </el-upload>
        </div> -->
        <div class="down">
          <div class="downleft">
            <div class="origin-div">
              <img v-if="originUrl" :src="originUrl" class="avatar">
              <div v-if="uploadFlag=='False'" class="el-upload__text">显示视频原帧</div>
            </div>
          </div>
          <div class="downright">
            <div class="detect-div">
              <img v-if="detectedUrl" :src="detectedUrl" class="avatar">
              <div v-if="uploadFlag=='False'" class="el-upload__text">显示检测结果</div>
            </div>
          </div>
        </div>
      </el-main>
      <el-footer>Copyright © 2020</el-footer>
    </el-container>
  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script>
export default {
  data(){
    return {
      value:'',
      options:[
        {
          value:'破洞',
          label:'破洞'
        },{
          value:'油污',
          label:'油污'
        },{
          value:'断纱1',
          label:'断纱1'
        },{
          value:'断纱2',
          label:'断纱2'
        },{
          value:'断纱3',
          label:'断纱3'
        },{
          value:'断纱4',
          label:'断纱4'
        }
      ],
      playerOptions : {
        playbackRates: [0.7, 1.0, 1.5, 2.0], //播放速度
        preload: true,
        autoplay: false, //如果true,浏览器准备好时开始回放。
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 导致视频一结束就重新开始。
        preload: 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [{
          type: "",
          src: '/src/static/破洞.mp4'//url地址          
          // src: "" //url地址
        }],
        poster: "", //你的封面地址
        // width: document.documentElement.clientWidth,
        notSupportedMessage: '请选择视频流', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
        controlBar: {
          timeDivider: true,
          durationDisplay: true,
          remainingTimeDisplay: false,
          fullscreenToggle: true  //全屏按钮
        }
      },
      tableData:[{class:'1',confidence:'0.1'}],
      uploadFlag:'False',
      originUrl:'',
      detectedUrl:'',
      // dialogImageUrl:'',
      imageUrl: '',
      random_num:'',
      // dialogVisible: false,
    };
  },
  methods: {
    startHacking () {
      this.$notify({
        title: 'It works!',
        type: 'success',
        message: 'We\'ve laid the ground work for you. It\'s time for you to build something epic!',
        duration: 5000
      })
    },
    handleAvatarSuccess(res, file) {
      console.log(res);
      this.imageUrl = URL.createObjectURL(file.raw);
      this.detectedUrl = res;
      this.uploadFlag = true;
      // this.$refs.response.src = res
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      if (!isJPG) {
        this.$message.error('Just support JPEG format');
      }
      return isJPG ;
    },
    selectModel(params){
      console.log(params);
      this.$http.post('http://166.111.180.117:8000/detectresult', {id:params}).then(
        (response) => {
          this.detectedUrl = response.data
          console.log(this.detectedUrl);
          this.uploadFlag = true;
          this.$message({
            message: '检测完成!',
            type: 'success'
          });
        })
      // this.$http.post('http://166.111.180.117:8000/getmodel', {id: params}).then(
      //   (response) => {
      //     if(response.data == 'success'){
      //       this.$message({
      //         message: 'Load model ended!',
      //         type: 'success'
      //       });
      //     }
      //   })
    },
    selectVideo(params){
      console.log(params);
      this.playerOptions.sources[0].src = '/src/static/'+String(params)+'.mp4';
      this.detectedUrl = '';
      this.originUrl = '';
    },
    detectDefect(player) {
      console.log(player.currentTime());
      this.$message({
        message: '正在检测，请稍等!',
        type: 'success'
      });
      // this.uploadFlag = true;
      // this.detectedUrl = '/src/static/'+'video_318.jpg';
      this.detectedUrl = '';
      this.originUrl = '';
      this.originload = true;
      this.detectload = true;
      this.$http.post('http://166.111.180.117:8000/detectresult', {id:player.currentTime(), videosrc:this.playerOptions.sources[0].src} ,{emulateJSON:true}).then(
        (response) => {
          this.random_num = response.data;
          console.log(this.random_num)
          this.originload = false;
          this.detectload = false;
          this.detectedUrl = '/src/static/result_mask_'+this.random_num+'.png';//response.data;
          this.originUrl = '/src/static/result_origin_'+this.random_num+'.png';
          // console.log(this.detectedUrl);
          this.uploadFlag = true;
          this.$message({
            message: '检测完成!',
            type: 'success'
          });
        });
      // console.log(this.$refs.videoPlayer.currentTime);
    },
  }
}
</script>

<style>
html,body,#app,.el-container,.home {
  padding: 0px;
  margin: 0px;
  height: 100%;
  /* font-family: Helvetica, sans-serif; */
  /* text-align: center; */
}
.el-header {
  background-color: #336699;
  color:#FFFFFF;
  font-family: "Helvetica Neue",Helvetica;
  font-size: 24px;
  text-align: left;
  line-height: 60px;
}
.el-footer {
  background-color: #336699;
  color: rgb(255, 255, 255);
  font-family: Helvetica;
  text-align: center;
  line-height: 60px;
}
.el-main {
  background-color: #a7c5f89a;
  /* background-color: #99CCFF; */
  color: #333;
  text-align: center;
  line-height: 160px;
}
.upleft {
  margin-top: 4%;
  margin-left:10%;
  float: left;
  width: 50%;
  height: 70%;
  background-color: rgba(255, 0, 0, 0);
  /* visibility:hidden; */
}
.upright {
  margin-top: 4%;
  margin-right: 9%;
  float: right;
  width: 27%;
  height: 70%;
  background-color: rgba(255, 0, 0, 0);
  /* visibility:hidden; */
}
.down{
  height: 100%;
}
.downleft {
  /* float: left; */
  display:inline;
  /* width: 50%;
  height: 100%; */
  background-color: rgba(255, 0, 0, 0);
  /* visibility:hidden; */
}
.downright {
  display:inline;
  /* float: right; */
  background-color: rgba(255, 166, 0, 0);
  /* margin-left: 0; */
  /* width: 70%;
  height: 100%; */
}
.detect_tag{
  color:#FFFFFF;
}
.el-row{
  height: 20px;
}
.el-col{
  font-family: Helvetica;
  height: 100%;
  margin-top: 5px;
}
.avatar-uploader .el-upload  {
  height: 43%;
  width: 43%;
  margin-left: 120px;
  margin-top: 45px;
  border: 1px dashed #336699;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}
.origin-div{
  float:left;
  height: 53%;
  width: 43%;
  margin-left: 7%;
  margin-top: 2%;
  border: 1px dashed #336699;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.detect-div{
  float:right;
  height: 53%;
  width: 43%;
  margin-top: 2%;
  margin-right: 5%;
  border: 1px dashed #336699;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.avatar-uploader .el-upload:hover {
  border-color:#FFFFFF;
}
.avatar {
    max-width: 100%;
    max-height: 100%;
    display: block;
  }
.el-upload__text{
  color:#FFFFFF;
}
.select-style .el-input__inner{
    background-color: rgba(255, 166, 0, 0) !important; 
}
  
.select-option{
  background-color: rgba(255, 166, 0, 0) !important; 
}
.select-option .el-select-dropdown__item.hover {
  background-color: rgba(110, 147, 206, 0.2);
  margin-right: 1px;
}
.video-player .vjs-custom-skin {
    width: 100%;
    height: 100%;
    display: block;
}

/* .detect-table{
  color:rgba(248, 78, 56, 0)
} */
/* .el-table__body tr{
  color:blue;
  height:30px;
}
.el-table__header tr,
  .el-table__header th {
    padding: 0;
    height: 0px;
} */
</style>
