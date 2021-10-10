'use strict'

const usage = { 
  template: '#usage',
  props:['usage','login']
}
const login = { 
  template: '#login',
  props: ['uasge','login']
}


const routes = [
  { path: '/usage', component: usage },
  { path: '/test', component: login }
]


const router = new VueRouter({
  mode: 'history',
  routes // `routes: routes` の短縮表記
})


const app = new Vue({
  el: '#appRoot',
  router,
  data() {
    return {
      //  appTitle: 'つぶやき書店',
      //  appLink1: 'TOP(つぶやき書店とは）',
      //  appLink2:'使い方',
      //  appLink3: '書店を利用する',
      //  appLink4: 'Github',
      isActive1: true,
      isActive2: false,
      // isActive3: false,
      // isActive4: false,
      topBody: true,
      HowtoUse: false,
      bLogin:false,
      navFlag:false,
      topFlag: true,
      topFlag2: false,
      topFlag3:true,
      hoverFlag: false,
      hoverIndex: null
    };
  },
  methods: {
    changeActive1: function () {
      this.isActive1 = true;
      this.isActive2 = false;
      // this.isActive3 = false;
      // this.isActive4 = false;
      this.topBody = true;
      this.HowtoUse = false;
      // this.bLogin = false;
      this.navFlag = false;
      this.topFlag = true;
      this.topFlag2 = false
    },
    changeActive2: function () {
      this.isActive1 = false;
      this.isActive2 = true;
      // this.isActive3 = false;
      // this.isActive4 = false;
      this.topBody = false;
      this.HowtoUse = true;
      // this.bLogin = false;
      this.navFlag = false;
      this.topFlag = false;
      this.topFlag2 = true;
      this.topFlag3 = false;
    },
    // changeActive3: function () {
    //   this.isActive1 = false;
    //   this.isActive2 = false;
    //   this.isActive3 = true;
    //   this.isActive4 = false;
    //   this.topBody = false;
    //   this.HowtoUse = false;
    //   this.bLogin = true;
    //   this.navFlag = false;
    // },
    // changeActive4: function () {
    //   this.isActive1 = false;
    //   this.isActive2 = false;
    //   this.isActive3 = false;
    //   this.isActive4 = true;
    //   this.topBody = false;
    //   this.HowtoUse = false;
    //   // this.bLogin = false;
    //   this.navFlag = false;
    // },
    navButton: function(){
      this.navFlag = !this.navFlag;
    },
    mouseOverAction:function(index){
      this.hoverFlag = true;
      this.hoverIndex = index;
    },
    mouseLeaveAction: function(){
      this.hoverFlag = false;
    }

  },
  delimiters: ['[[', ']]']
})
