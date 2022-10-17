(self["webpackChunkpython_qrcode_web"]=self["webpackChunkpython_qrcode_web"]||[]).push([[512],{91191:function(e,a,s){"use strict";s.r(a),s.d(a,{default:function(){return D}});s(96651);var r=s(29245),t=(s(22162),s(76774)),n=(s(94513),s(80003)),c=(s(63639),s(51620)),i=(s(79845),s(11983)),l=(s(14730),s(69672)),d=(s(91204),s(76997)),u=s(57113),o=(s(49404),s(52306)),p=s(82005),m=s(71188),h=s(50959),x=s(11527),v=()=>(0,x.jsx)("div",{className:"navbar",children:(0,x.jsx)("div",{className:"navbar-box",children:(0,x.jsx)("span",{className:"navbar-title",children:"Python_QRCode WebUI"})})}),b=v,j=s(46090),f=s.n(j),Z=[200],g={timeout:1e5,headers:{"Content-type":"application/json"},baseURL:"http://127.0.0.1:5000"},w=e=>{var a=e.status,s=e.data;if(!Z.includes(a)||0!==s.code)throw s.message;return s},N=e=>{var a,s=e.response;throw null!==s&&void 0!==s&&null!==(a=s.data)&&void 0!==a&&a.message?s.data.message:e},k=f().create(g);k.interceptors.response.use(w,N);var y=k;function C(e){return S.apply(this,arguments)}function S(){return S=(0,p.Z)((0,u.Z)().mark((function e(a){var s,r,t;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return s="/api/encode",e.next=3,y.post(s,a);case 3:return r=e.sent,t=r.data,e.abrupt("return",t);case 6:case"end":return e.stop()}}),e)}))),S.apply(this,arguments)}function q(e){return U.apply(this,arguments)}function U(){return U=(0,p.Z)((0,u.Z)().mark((function e(a){var s,r,t;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return s="/api/decode",e.next=3,y.post(s,a);case 3:return r=e.sent,t=r.data,e.abrupt("return",t);case 6:case"end":return e.stop()}}),e)}))),U.apply(this,arguments)}var _=(e,a)=>{var s=document.createElement("a");s.href=e,s.download=a,s.click()},R=()=>{var e=(0,h.useState)(""),a=(0,m.Z)(e,2),s=a[0],v=a[1],j=(0,h.useState)(""),f=(0,m.Z)(j,2),Z=f[0],g=f[1],w=(0,h.useState)(!1),N=(0,m.Z)(w,2),k=N[0],y=N[1],S=(0,h.useState)(""),U=(0,m.Z)(S,2),R=U[0],D=U[1],L=(0,h.useState)(""),P=(0,m.Z)(L,2),A=P[0],G=P[1],I=(0,h.useState)(!1),T=(0,m.Z)(I,2),z=T[0],B=T[1],E=function(){var e=(0,p.Z)((0,u.Z)().mark((function e(a){var s,r,t,n,c;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(s="image/jpeg"===a.type,r="image/png"===a.type,s||r){e.next=5;break}return o.default.error("You can only upload JPG/PNG file!"),e.abrupt("return",!1);case 5:if(t=a.size/1024/1024<5,t){e.next=9;break}return o.default.error("Image must smaller than 2MB!"),e.abrupt("return",!1);case 9:n="",c=new FileReader,c.readAsDataURL(a),c.onload=(0,p.Z)((0,u.Z)().mark((function e(){var a;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return a=c.result,n=a.replace("data:image/png;base64,",""),D(n),e.abrupt("return",!1);case 4:case"end":return e.stop()}}),e)})));case 13:case"end":return e.stop()}}),e)})));return function(a){return e.apply(this,arguments)}}(),F=function(){var e=(0,p.Z)((0,u.Z)().mark((function e(){var a;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:return y(!0),e.prev=1,e.next=4,C({data:s});case 4:a=e.sent,g("data:image/png;base64,".concat(a)),o.default.success("\u751f\u6210\u6210\u529f"),e.next=12;break;case 9:e.prev=9,e.t0=e["catch"](1),console.error(e.t0);case 12:y(!1);case 13:case"end":return e.stop()}}),e,null,[[1,9]])})));return function(){return e.apply(this,arguments)}}(),J=function(){var e=(0,p.Z)((0,u.Z)().mark((function e(){var a;return(0,u.Z)().wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(R){e.next=2;break}return e.abrupt("return");case 2:return B(!0),e.prev=3,e.next=6,q({data:R});case 6:a=e.sent,G(null===a||void 0===a?void 0:a[0]),o.default.success("\u89e3\u7801\u6210\u529f"),e.next=14;break;case 11:e.prev=11,e.t0=e["catch"](3),console.error(e.t0);case 14:B(!1);case 15:case"end":return e.stop()}}),e,null,[[3,11]])})));return function(){return e.apply(this,arguments)}}(),M=()=>{var e="output-".concat((new Date).getTime(),".png");_(Z,e)};return(0,x.jsxs)("div",{className:"container",children:[(0,x.jsx)(b,{}),(0,x.jsxs)(r.Z,{className:"qr",children:[(0,x.jsx)(c.Z,{className:"qr-card",span:8,children:(0,x.jsxs)("div",{className:"encode",children:[(0,x.jsx)(d.Z.TextArea,{rows:4,allowClear:!0,className:"encode-input",placeholder:"\u8bf7\u8f93\u5165\u8981\u7f16\u7801\u7684\u5185\u5bb9",onChange:e=>v(e.target.value)}),(0,x.jsx)("div",{className:"encode-img",children:""===Z?(0,x.jsx)("div",{className:"empty-img-box",children:k&&(0,x.jsx)(l.Z,{})}):(0,x.jsx)("div",{className:"img-box",children:k?(0,x.jsx)(l.Z,{}):(0,x.jsx)("img",{className:"image",src:Z})})}),(0,x.jsxs)("div",{children:[(0,x.jsx)(i.Z,{className:"encode-btn",onClick:()=>F(),disabled:""===s||k,children:(0,x.jsx)("span",{className:"encode-btn-text",children:"\u751f\u6210"})}),(0,x.jsx)(i.Z,{type:"primary",className:"encode-btn",onClick:()=>M(),disabled:""===s||k,children:(0,x.jsx)("span",{className:"encode-btn-text",children:"\u4fdd\u5b58"})})]})]})}),(0,x.jsx)(c.Z,{className:"qr-card",span:8,children:(0,x.jsxs)("div",{className:"decode",children:[(0,x.jsx)("div",{className:"decode-img",children:(0,x.jsx)(n.Z.Dragger,{showUploadList:!1,beforeUpload:E,children:(0,x.jsx)("div",{className:"img-box",children:""===R?(0,x.jsx)("div",{className:"empty-img-box-upload"}):(0,x.jsxs)("div",{className:"mask-box",children:[(0,x.jsx)("img",{className:"image",src:"data:image/png;base64,".concat(R)}),(0,x.jsx)("div",{className:"mask",children:(0,x.jsx)(i.Z,{children:"\u66f4\u65b0"})})]})})})}),(0,x.jsx)("div",{className:"decode-output",children:z?(0,x.jsx)(l.Z,{}):(0,x.jsx)(t.Z,{placement:"top",title:A,children:(0,x.jsx)("span",{className:"output-text",children:A})})}),(0,x.jsx)(i.Z,{type:"primary",className:"decode-btn",onClick:()=>J(),children:(0,x.jsx)("span",{className:"decode-btn-text",children:"\u8bc6\u522b"})})]})})]}),(0,x.jsx)("div",{className:"bg"})]})},D=R}}]);