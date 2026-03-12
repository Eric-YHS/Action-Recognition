// miniprogram/pages/test/test.js
const db = wx.cloud.database()
const _ = db.command

Page({

  /**
   * 页面的初始数据
   */
  data: {
    selecttype: ["点击选择", "ios", "安卓"],
    accxn: [],
    accyn: [],
    acczn: [],
    gyrxn: [],
    gyryn: [],
    gyrzn: [],
    start: false,
    tag: false,
    result: '0',
    resultold: '0',
    play: true,
    step: 3,
    counttime: 0,
    countnum1: 0,
    countnum2: 0,
    countnum3: 0,
    countnum4: 0,
    temptype: '点击选择',
    type: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    this.onUnload()
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    this.setData({
      start: false,
      tag: false,
      result: '0',
      counttime: 0,
      countnum1: 0,
      countnum2: 0,
      countnum3: 0,
      countnum4: 0,
    })
    wx.offAccelerometerChange()
    wx.offGyroscopeChange()
    clearInterval(this.loop1)
    clearInterval(this.loop2)
    clearInterval(this.loop3)
    if (this.innerAudioContext1 != undefined) {
      this.innerAudioContext1.destroy()
    }
    if (this.innerAudioContext2 != undefined) {
      this.innerAudioContext2.destroy()
    }
    if (this.innerAudioContext3 != undefined) {
      this.innerAudioContext3.destroy()
    }
    wx.request({
      url: 'https://www.inifyy.cn:8080/clear',
      method: "post",
    })
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  startTest() {
    var _this = this;
    var num1 = 0;
    var num2 = 0;
    let accXs = [];
    let accYs = [];
    let accZs = [];
    let gyrXs = [];
    let gyrYs = [];
    let gyrZs = [];
    let typeselect = ["game", "ui"]
    let typenum = [50, 17]
    var num = typenum[this.data.type-1]

    if (this.data.type != 0){
      wx.startAccelerometer({
        interval: typeselect[this.data.type-1]
      })
      wx.startGyroscope({
        interval: typeselect[this.data.type-1]
      })
      wx.onGyroscopeChange(function (res) {
        gyrXs.push(res.x)
        gyrYs.push(res.y)
        gyrZs.push(res.z)
        num1++
        if (num1 >= num) {
          wx.offGyroscopeChange()
          _this.setData({
            num1: num1,
            gyrxo: _this.data.gyrxn,
            gyryo: _this.data.gyryn,
            gyrzo: _this.data.gyrzn,
            gyrxn: gyrXs,
            gyryn: gyrYs,
            gyrzn: gyrZs,
          })
        }
      })
      wx.onAccelerometerChange(function (res) {
        accXs.push(res.x)
        accYs.push(res.y)
        accZs.push(res.z)
        num2++
        if (num2 >= num) {
          wx.offAccelerometerChange()
          _this.setData({
            num2: num2,
            accxo: _this.data.accxn,
            accyo: _this.data.accyn,
            acczo: _this.data.acczn,
            accxn: accXs,
            accyn: accYs,
            acczn: accZs,
          })
        }
      })
    }
  },

  stopTest: function () {
    var _this = this
    this.innerAudioContext3 = wx.createInnerAudioContext()
    this.innerAudioContext3.loop = false
    wx.setInnerAudioOption({
      obeyMuteSwitch: false,
    })
    this.setData({
      start: false,
      tag: false,
      counttime: 0,
      result: '0',
    })
    wx.offAccelerometerChange()
    wx.offGyroscopeChange()
    clearInterval(this.loop1)
    clearInterval(this.loop2)
    clearInterval(this.loop3)

    this.innerAudioContext3.src = 'cloud://charlie-mf4i1.6368-charlie-mf4i1-1301400124/finish.mp3';
    this.innerAudioContext3.autoplay = true
    setTimeout(function () {
      if (this.innerAudioContext1 != undefined) {
        this.innerAudioContext1.destroy()
      }
      if (this.innerAudioContext2 != undefined) {
        this.innerAudioContext2.destroy()
      }
      _this.innerAudioContext3.destroy()
    }, 3000)
    wx.request({
      url: 'https://www.inifyy.cn:8080/clear',
      method: "post",
    })
  },

  sendTest: function () {
    var _this = this
    if (this.data.tag == false) {
      if (this.data.type != 0){
        this.setData({
          tag: true,
          countnum1: 0,
          countnum2: 0,
          countnum3: 0,
          countnum4: 0,
        })
        this.innerAudioContext1 = wx.createInnerAudioContext()
        this.innerAudioContext1.loop = false
        wx.setInnerAudioOption({
          obeyMuteSwitch: false,
        })
        this.innerAudioContext1.src = 'cloud://charlie-mf4i1.6368-charlie-mf4i1-1301400124/start.mp3';
        this.innerAudioContext1.autoplay = true
  
        _this.loop1 = setInterval(function () {
          _this.startTest()
          setTimeout(function () {
            if (_this.data.start == true) {
              wx.request({
                url: 'https://www.inifyy.cn:8080',
                header: {
                  'content-type': 'application/json'
                },
                data: {
                  accx: _this.data.accxo + ',' + _this.data.accxn,
                  accy: _this.data.accyo + ',' + _this.data.accyn,
                  accz: _this.data.acczo + ',' + _this.data.acczn,
                  gyrx: _this.data.gyrxo + ',' + _this.data.gyrxn,
                  gyry: _this.data.gyryo + ',' + _this.data.gyryn,
                  gyrz: _this.data.gyrzo + ',' + _this.data.gyrzn,
                  type: _this.data.type,
                },
                method: "post",
                success(res) {
                  _this.setData({
                    result: res.data,
                  })
                },
              })
            } else {
              wx.request({
                url: 'https://www.inifyy.cn:8080/clear',
                method: "post",
              })
              _this.setData({
                start: true,
              })
              _this.innerAudioContext2.destroy()
            }
          }, 1050)
        }, 1100)
  
        _this.loop3 = setInterval(function () {
          if(_this.data.counttime == 0 || Number(_this.data.resultold) == 0){
            _this.setData({
              counttime: _this.data.counttime + 1,
            })
          }else{
            wx.request({
              url: 'https://www.inifyy.cn:8080/count',
              method: "post",
              data: {
                type: _this.data.type,
              },
              success(res) {
                var temp = res.data.slice(1,-2).split(". ")
                _this.setData({
                  countnum1: Number(temp[0]),
                  countnum2: Number(temp[1]),
                  countnum3: Number(temp[2]),
                  countnum4: Number(temp[3]),
                })
              },
            })
          }
          _this.setData({
            resultold: _this.data.result,
          })
        },4400)
  
        if (_this.data.play == true) {
          _this.loop2 = setInterval(function () {
            if (_this.data.result != '0') {
              _this.innerAudioContext2 = wx.createInnerAudioContext()
              _this.innerAudioContext2.loop = false
              wx.setInnerAudioOption({
                obeyMuteSwitch: false,
              })
              _this.innerAudioContext2.src = 'cloud://charlie-mf4i1.6368-charlie-mf4i1-1301400124/activity' + _this.data.result + '.mp3';
              _this.innerAudioContext2.autoplay = true
              setTimeout(function () {
                _this.innerAudioContext2.destroy()
              }, 1500)
            }
          }, 3000)
        }
      }else{
        wx.showToast({
          icon: 'none',
          title: '请选择手机对应的系统！',
        })
      }
    }
  },

  voiceControl: function (res) {
    this.setData({
      play: ~this.data.play
    })
    if (this.data.play == false) {
      clearInterval(this.loop2)
    }
  },

  stepSelect: function (res) {
    var array = ["点击选择", "ios", "安卓"]
    var t = array[Number(res.detail.value)]
    this.setData({
      temptype: t,
      type: Number(res.detail.value),
    })
  },

  problem: function () {
    wx.showModal({
      title: '问题反馈',
      content: '如小程序技术故障，或其他问题咨询，请私戳qq：986765210',
    })
  }
})