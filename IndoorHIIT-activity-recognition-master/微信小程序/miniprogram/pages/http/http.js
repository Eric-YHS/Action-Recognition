// miniprogram/pages/http/http.js
const db = wx.cloud.database()
const _ = db.command

Page({

  /**
   * 页面的初始数据
   */
  data: {
    result: '',
    value: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {
    db.collection('data').where({
      activity:1,
    }).count({
      success: res => {
        this.setData({
          activity1: res.total
        })
      }
    })
    db.collection('data').where({
      activity: 2,
    }).count({
      success: res => {
        this.setData({
          activity2: res.total
        })
      }
    })
    db.collection('data').where({
      activity: 3,
    }).count({
      success: res => {
        this.setData({
          activity3: res.total
        })
      }
    })
    db.collection('data').where({
      activity: 4,
    }).count({
      success: res => {
        this.setData({
          activity4: res.total
        })
      }
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

  sendmsg: function() {
    var _this = this
    wx.request({
      url: 'https://www.inifyy.cn:8080',
      data: {
        data: this.data.value,
      },
      method: "post",
      success(res) {
        _this.setData({
          result: res.data,
        })
        console.log(res.data)
      },
      fail(res) {
        console.log('fail')
      }
    })
  },

  inputvalue: function(res) {
    this.setData({
      value: res.detail.value,
    })
  },
})