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
  { path: '/login', component: login }
]


const router = new VueRouter({
  mode: 'history',
  routes // `routes: routes` の短縮表記
})


var app = new Vue({
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
      isActive3: false,
      isActive4: false,
      topBody: true,
      HowtoUse: false,
      bLogin:false,
      navFlag:false
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
      this.navFlag = false;
    },
    changeActive2: function () {
      this.isActive1 = false;
      this.isActive2 = true;
      this.isActive3 = false;
      this.isActive4 = false;
      this.topBody = false;
      this.HowtoUse = true;
      this.bLogin = false;
      this.navFlag = false;
    },
    changeActive3: function () {
      this.isActive1 = false;
      this.isActive2 = false;
      this.isActive3 = true;
      this.isActive4 = false;
      this.topBody = false;
      this.HowtoUse = false;
      this.bLogin = true;
      this.navFlag = false;
    },
    changeActive4: function () {
      this.isActive1 = false;
      this.isActive2 = false;
      this.isActive3 = false;
      this.isActive4 = true;
      this.topBody = false;
      this.HowtoUse = false;
      this.bLogin = false;
      this.navFlag = false;
    },
    navButton: function(){
      this.navFlag = !this.navFlag;
    }

  },
  delimiters: ['[[', ']]']
})
