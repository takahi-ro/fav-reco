'use strict'
// Vue.component('app-header',{
//     template: '#header',
//     props : ['link1','link2','link3','link4','logo'],
//     delimiters: ['[[', ']]']
//   })


var app = new Vue({
  el: '#appRoot',
  data() {
    return {
      //  appTitle: 'つぶやき書店',
      //  appLink1: 'TOP(つぶやき書店とは）',
      //  appLink2:'使い方',
      //  appLink3: '書店を利用する',
      //  appLink4: 'Github',
      isActive1: true,
      isActive2: false,
      isActive3: false,
      isActive4: false,
      topBody: true,
      HowtoUse: false,
      bLogin:false
    };
  },
  methods: {
    changeActive1: function () {
      this.isActive1 = true;
      this.isActive2 = false;
      this.isActive3 = false;
      this.isActive4 = false;
      this.topBody = true;
      this.HowtoUse = false;
      this.bLogin = false;
    },
    changeActive2: function () {
      this.isActive1 = false;
      this.isActive2 = true;
      this.isActive3 = false;
      this.isActive4 = false;
      this.topBody = false;
      this.HowtoUse = true;
      this.bLogin = false;
    },
    changeActive3: function () {
      this.isActive1 = false;
      this.isActive2 = false;
      this.isActive3 = true;
      this.isActive4 = false;
      this.topBody = false;
      this.HowtoUse = false;
      this.bLogin = true;
    },
    changeActive4: function () {
      this.isActive1 = false;
      this.isActive2 = false;
      this.isActive3 = false;
      this.isActive4 = true;
      this.topBody = false;
      this.HowtoUse = false;
      this.bLogin = false;
    }

  },
  delimiters: ['[[', ']]']
})
