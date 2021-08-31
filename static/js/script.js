'use strict'
Vue.component('app-header',{
    template: '#header',
    props : ['link1','link2'],
    delimiters: ['[[', ']]']
  })


  var app =  new Vue({
     el: '#appRoot',
     data : {
       appTitle: 'fav-reco',
       appLink1: 'HOME',
       appLink2: 'LOGIN'
     },
     delimiters: ['[[', ']]']
   })
