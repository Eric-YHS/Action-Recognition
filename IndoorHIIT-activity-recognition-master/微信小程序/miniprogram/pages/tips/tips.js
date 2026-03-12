// miniprogram/pages/tips/tips.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    activity: 0,
    actname: '',
    imgsrc: '',
    name: '',
    age: '',
    height: '',
    type: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    const act = ['徒手侧平举', '前后交叉小跑', '开合跳', '半蹲']
    const colorchoose = ['#FF7F8C', '#19EEBE', '#F8CE17', '#4D98FE']
    this.setData({
      activity: options.activity,
      name: options.name,
      age: options.age,
      height: options.height,
      type: options.type,
      color: colorchoose[options.activity - 1],
      actname: act[options.activity - 1],
      imgsrc: '../image/activity' + options.activity + '.gif'
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

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

  startGet: function() {
    wx.redirectTo({
      url: '../record/record?activity=' + this.data.activity + '&name=' + this.data.name + '&age=' + this.data.age + '&height=' + this.data.height + '&type=' + this.data.type,
    })
  }
})