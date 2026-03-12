// miniprogram/pages/home/home.js
const db = wx.cloud.database()
const _ = db.command

Page({

  /**
   * 页面的初始数据
   */
  data: {
    name: '',
    heightselect: ["点击选择", "150以下", "151-155", "156-160", "161-165", "166-170", "171-175", "176-180", "181-185", "186-190", "190以上"],
    ageselect: ["点击选择", "15及以下", "16-25", "26-35", "36-45", "46-55", "55以上"],
    typeselect: ["点击选择", "ios系统", "安卓系统"],
    age: '点击选择',
    height: '点击选择',
    type: '点击选择',
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

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

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

  agechange: function (res) {
    this.setData({
      age: this.data.ageselect[res.detail.value]
    })
  },

  heightchange: function (res) {
    this.setData({
      height: this.data.heightselect[res.detail.value]
    })
  },

  typechange: function (res) {
    this.setData({
      type: this.data.typeselect[res.detail.value]
    })
  },

  nameFun: function (res) {
    this.setData({
      name: res.detail.value,
    })
    console.log(res.detail.value)
  },

  chooseWhich1: function () {
    if (this.data.type == '点击选择') {
      wx.showToast({
        icon: 'none',
        title: '请填写手机型号！',
      })
    } else {
      if (this.data.type == 'ios系统') {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 1 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 1,
        })
      } else {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 1 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 2,
        })
      }
    }
  },

  chooseWhich2: function () {
    if (this.data.type == '点击选择') {
      wx.showToast({
        icon: 'none',
        title: '请填写手机型号！',
      })
    } else {
      if (this.data.type == 'ios系统') {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 2 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 1,
        })
      } else {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 2 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 2,
        })
      }
    }
  },

  chooseWhich3: function () {
    if (this.data.type == '点击选择') {
      wx.showToast({
        icon: 'none',
        title: '请填写手机型号！',
      })
    } else {
      if (this.data.type == 'ios系统') {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 3 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 1,
        })
      } else {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 3 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 2,
        })
      }
    }
  },

  chooseWhich4: function () {
    if (this.data.type == '点击选择') {
      wx.showToast({
        icon: 'none',
        title: '请填写手机型号！',
      })
    } else {
      if (this.data.type == 'ios系统') {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 4 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 1,
        })
      } else {
        wx.navigateTo({
          url: '../tips/tips?activity=' + 4 + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + 2,
        })
      }
    }
  },

  gotoExplain: function () {
    db.collection('control').get({
      success: res => {
        if (res.data[0].entry2 == true) {
          wx.navigateTo({
            url: '../http/http',
          })
        } else {
          wx.showToast({
            icon: 'none',
            title: '您暂无权限 （^v^）',
          })
        }
      }
    })

  }
})