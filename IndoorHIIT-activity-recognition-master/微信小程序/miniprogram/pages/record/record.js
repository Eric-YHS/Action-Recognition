// miniprogram/pages/record/record.js
const db = wx.cloud.database()
const _ = db.command

Page({

  /**
   * 页面的初始数据
   */
  data: {
    accxsum: [],
    accysum: [],
    acczsum: [],
    gryxsum: [],
    gryysum: [],
    gryzsum: [],
    count: 0,
    commit: 3,
    number: 0,
    type: 0,
    way: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.setData({
      activity: options.activity,
      name: options.name,
      age: options.age,
      height: options.height,
      type: options.type,
    })
    if(options.type == 1){
      this.setData({
        way: 'game',
      })
    } else if (options.type == 2){
      this.setData({
        way: 'ui',
      })
    }else{}
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {
    var _this = this;
    var num = 0;
    let accXs = [];
    let accYs = [];
    let accZs = [];
    let gyrXs = [];
    let gyrYs = [];
    let gyrZs = [];

    this.setData({
      commit: 3,
    })

    this.innerAudioContext = wx.createInnerAudioContext()
    // innerAudioContext.autoplay = true
    this.innerAudioContext.loop = false // 是否循环播放，默认为 false
    wx.setInnerAudioOption({ // ios在静音状态下能够正常播放音效
      obeyMuteSwitch: false, // 是否遵循系统静音开关，默认为 true。当此参数为 false 时，即使用户打开了静音开关，也能继续发出声音。
    })
    this.innerAudioContext.src = 'cloud://charlie-mf4i1.6368-charlie-mf4i1-1301400124/record.mp3'; // 音频资源的地址
    this.innerAudioContext.autoplay = true
    this.innerAudioContext.onPlay(() => { // 监听音频播放事件
      this.setData({
        commit: 0,
      })
      setTimeout(function() {
        wx.startAccelerometer({
          interval: _this.data.way
        })
        wx.startGyroscope({
          interval: _this.data.way
        })
        wx.onGyroscopeChange(function(res) {
          gyrXs.push(res.x)
          gyrYs.push(res.y)
          gyrZs.push(res.z)
          num++
        })
        wx.onAccelerometerChange(function(res) {
          accXs.push(res.x)
          accYs.push(res.y)
          accZs.push(res.z)
        })
      }, 5000);
    })

    this.innerAudioContext.onEnded(() => {
      wx.stopAccelerometer()
      wx.stopGyroscope()
      wx.offGyroscopeChange()
      wx.offAccelerometerChange()
      _this.setData({
        gryxsum: gyrXs,
        gryysum: gyrYs,
        gryzsum: gyrZs,
      })
      _this.setData({
        accxsum: accXs,
        accysum: accYs,
        acczsum: accZs,
        count: num,
        time: Date.parse(new Date()),
        commit: 1,
      })
    })
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {
    this.innerAudioContext.destroy()
    wx.offGyroscopeChange()
    wx.offAccelerometerChange()
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  savedata: function() {
    var _this = this;
    if (this.data.commit == 1) {
      if (this.data.number > 0 && this.data.number < 30){
        wx.showModal({
          title: '提交数据',
          content: '您是否确认提交数据',
          success(res) {
            if (res.confirm) {
              wx.showToast({
                icon: 'none',
                title: '提交中，请等待5-10秒，请勿退出',
              })
              db.collection('data').add({
                data: {
                  name: _this.data.name,
                  age: _this.data.age,
                  height: _this.data.height,
                  activity: Number(_this.data.activity),
                  time: _this.data.time,
                  number: Number(_this.data.number),
                  type: Number(_this.data.type),
                }, success: res => {
                  db.collection('data').doc(res._id).update({
                    data: {
                      gryy: _this.data.gryysum,
                      gryz: _this.data.gryzsum,
                    },
                    fail(res) {
                      console.log(res)
                      wx.showToast({
                        icon: 'none',
                        title: '提交失败，请重试',
                      })
                    }
                  })

                  db.collection('data').doc(res._id).update({
                    data: {
                      accy: _this.data.accysum,
                      accz: _this.data.acczsum,
                    },
                    fail(res) {
                      console.log(res)
                      wx.showToast({
                        icon: 'none',
                        title: '提交失败，请重试',
                      })
                    }
                  })

                  db.collection('data').doc(res._id).update({
                    data: {
                      accx: _this.data.accxsum,
                      gryx: _this.data.gryxsum,
                    }, success(res) {
                      _this.setData({
                        commit: 2,
                        number: 0,
                      })
                      wx.showToast({
                        icon: 'none',
                        title: '提交成功！',
                      })
                    }, fail(res) {
                      console.log(res)
                      wx.showToast({
                        icon: 'none',
                        title: '提交失败，请重试',
                      })
                    }
                  })
                }, fail(res) {
                  console.log(res)
                  wx.showToast({
                    icon: 'none',
                    title: '提交失败，请重试',
                  })
                }
              })
            }
          }
        })
      }else{
        wx.showToast({
          icon: 'none',
          title: '请重新填写动作次数~',
        })
      }
    } else if (this.data.commit == 2) {
      wx.showToast({
        icon: 'none',
        title: '您已提交过本次数据了哦',
      })
    } else {
      wx.showToast({
        icon: 'none',
        title: '您还未完成采集',
      })
    }
  },

  redata: function() {
    var _this = this
    wx.showModal({
      title: '重新采集',
      content: '是否重新开始采集？',
      success(res) {
        if (res.confirm) {
          _this.innerAudioContext.destroy()
          wx.offGyroscopeChange()
          wx.offAccelerometerChange()
          _this.onReady(true);
        }
      }
    })
  },

  giveup: function() {
    wx.showModal({
      title: '放弃采集',
      content: '是否放弃本次采集？',
      success: res => {
        if (res.confirm) {
          wx.offGyroscopeChange()
          wx.offAccelerometerChange()
          wx.navigateBack({
            url: '../home/home',
          })
        }
      },
    })
  },

  numberFun: function (res) {
    this.setData({
      number: res.detail.value
    })
  }
})


