// miniprogram/pages/explain/explain.js
const db = wx.cloud.database()
const _ = db.command

Page({

  /**
   * 页面的初始数据
   */
  data: {
    gate: false,
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
    var _this = this

    db.collection('control').get({
      success: res => {
        _this.setData({
          gate: res.data[0].entry1,
        })
      }
    })
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
    this.setData({
      enter: 0,
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

  gotoHome: function () {
    wx.navigateTo({
      url: '../home/home',
    })
  },

  gotoTest: function () {
    if (this.data.gate == true) {
      wx.navigateTo({
        url: '../test/test',
      })
    } else {
      wx.showToast({
        icon: 'none',
        title: '测试入口暂未开放~',
      })
    }
  }
})