<template>
  <nav
    v-bind:class="navClass"
    v-on:mouseleave.passive="leaveMenu()"
    v-on:mouseover.passive="isOverMenu = true"
  >
    <ul class="cell auto" v-bind:class="adminSubmenuShown ? 'submenu shown' : 'submenu hidden'">
      <li class="close-item" v-on:click="closeMenus(true)"><button type="button" class="close-button">&times;</button></li>
      <li><router-link to="/Offices">Отделения</router-link></li>
      <li><router-link to="/ServiceTypes">Услуги</router-link></li>
      <li><router-link to="/GoodsTypes">Товары</router-link></li>
      <li><router-link to="/ExpenseTypes">Типы расходов</router-link></li>
      <li><router-link to="/EmployeePaymentTypes">Типы выплат сотрудникам</router-link></li>
      <li><router-link to="/Employees">Сотрудники</router-link></li>
      <li><router-link to="/MasterTypes">Категории мастеров</router-link></li>
    </ul>
    <ul v-bind:class="reportsSubmenuShown ? 'submenu shown' : 'submenu hidden'">
      <li class="close-item" v-on:click="closeMenus(true)"><button type="button" class="close-button">&times;</button></li>
      <li><router-link to="/EmployeesReport">Отчёт по сотрудникам</router-link></li>
      <li><router-link to="/ClientsReport">Отчёт по клиентам</router-link></li>
      <li><router-link to="/FinancialReport">Финансовый отчёт</router-link></li>
      <li><router-link to="/UploadExpenses">Загрузка расходов</router-link></li>
    </ul>
    <ul>
      <li
        v-bind:class="selectedElement === 'session' ? 'selected' : ''"
        v-on:mouseenter.passive="enterNoSubmenuEl()"
        v-on:mouseleave.passive="isOverNoSubmenuEl = false"
      >
        <router-link to="/">
          <svg class="main-menu-icon" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M20 40C31.0457 40 40 31.0457 40 20C40 8.9543 31.0457 0 20 0C8.9543 0 0 8.9543 0 20C0 31.0457 8.9543 40 20 40ZM20 36.5217C29.1247 36.5217 36.5217 29.1247 36.5217 20C36.5217 10.8753 29.1247 3.47826 20 3.47826C10.8753 3.47826 3.47826 10.8753 3.47826 20C3.47826 29.1247 10.8753 36.5217 20 36.5217Z" v-bind:fill="selectedElement === 'session' ? '#FDFCFC' : '#38342E'"/>
            <path d="M22.8986 20C22.8986 21.6008 21.6008 22.8986 20 22.8986C18.3992 22.8986 17.1014 21.6008 17.1014 20C17.1014 18.3992 18.3992 17.1014 20 17.1014C21.6008 17.1014 22.8986 18.3992 22.8986 20Z" v-bind:fill="selectedElement === 'session' ? '#FDFCFC' : '#38342E'"/>
            <path d="M20.8387 18.226C21.5283 18.8945 21.5455 19.9955 20.877 20.6852C20.2085 21.3749 19.1075 21.3921 18.4178 20.7236L13.4227 15.8819C12.733 15.2134 12.7158 14.1124 13.3843 13.4227C14.0528 12.733 15.1539 12.7158 15.8435 13.3843L20.8387 18.226Z" v-bind:fill="selectedElement === 'session' ? '#FDFCFC' : '#38342E'"/>
            <path d="M30.0853 12.4165C30.6349 12.088 31.3468 12.2673 31.6753 12.8169C32.0038 13.3666 31.8245 14.0784 31.2749 14.4069L20.8252 20.6525C20.2755 20.981 19.5636 20.8017 19.2351 20.2521C18.9066 19.7025 19.0859 18.9906 19.6355 18.6621L30.0853 12.4165Z" v-bind:fill="selectedElement === 'session' ? '#FDFCFC' : '#38342E'"/>
          </svg>
          <label>Смена</label>
        </router-link>
      </li>
      <li
        v-bind:class="selectedElement === 'clients' ? 'selected' : ''"
        v-on:mouseenter.passive="enterNoSubmenuEl()"
        v-on:mouseleave.passive="isOverNoSubmenuEl = false"
      >
        <router-link to="/Clients">
          <svg class="main-menu-icon" viewBox="0 0 34 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M16.6527 19.9163C22.1525 19.9163 26.6109 15.4579 26.6109 9.95816C26.6109 4.45842 22.1525 0 16.6527 0C11.153 0 6.69456 4.45842 6.69456 9.95816C6.69456 15.4579 11.153 19.9163 16.6527 19.9163ZM16.6527 16.9038C20.4887 16.9038 23.5983 13.7941 23.5983 9.95816C23.5983 6.12221 20.4887 3.01255 16.6527 3.01255C12.8168 3.01255 9.70711 6.12221 9.70711 9.95816C9.70711 13.7941 12.8168 16.9038 16.6527 16.9038Z" v-bind:fill="selectedElement === 'clients' ? '#FDFCFC' : '#38342E'"/>
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5.48354 22.4455C3.95261 23.9909 3.01255 26.1093 3.01255 28.4519C3.01255 33.1659 6.83405 36.9874 11.5481 36.9874H21.9247C26.6387 36.9874 30.4602 33.1659 30.4602 28.4519C30.4602 26.069 29.4874 23.9175 27.9092 22.3657C27.8771 22.3775 27.8405 22.3926 27.7999 22.412C27.6784 22.47 27.5482 22.5532 27.4258 22.657C24.5233 25.1214 20.7581 26.6109 16.6527 26.6109C12.5906 26.6109 8.86116 25.1526 5.97115 22.7342C5.84761 22.6308 5.7161 22.5482 5.59338 22.4909C5.5526 22.4719 5.51585 22.457 5.48354 22.4455ZM3.61116 20.0635C4.80923 18.9296 6.63933 19.3652 7.90445 20.4239C10.2726 22.4055 13.3233 23.5983 16.6527 23.5983C20.0174 23.5983 23.0975 22.3801 25.4761 20.3606C26.7281 19.2975 28.5447 18.8476 29.7521 19.9612C32.0398 22.0713 33.4728 25.0942 33.4728 28.4519C33.4728 34.8297 28.3025 40 21.9247 40H11.5481C5.17027 40 0 34.8297 0 28.4519C0 25.1481 1.38732 22.1684 3.61116 20.0635Z" v-bind:fill="selectedElement === 'clients' ? '#FDFCFC' : '#38342E'"/>
          </svg>
          <label>Клиенты</label>
        </router-link>
      </li>
      <li
        v-bind:class="selectedElement === 'history' ? 'selected' : ''"
        v-on:mouseenter.passive="enterNoSubmenuEl()"
        v-on:mouseleave.passive="isOverNoSubmenuEl = false"
      >
        <router-link to="/SessionsHistory">
          <svg class="main-menu-icon" viewBox="0 0 40 38" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21.2034 33.7265C29.4489 33.7265 36.1333 27.0422 36.1333 18.7966C36.1333 10.5511 29.4489 3.86675 21.2034 3.86675C12.9578 3.86675 6.27348 10.5511 6.27348 18.7966C6.27348 19.7609 6.36488 20.7038 6.53951 21.6171C4.39123 21.6171 2.47413 20.0852 2.47329 17.9369C2.47205 14.7476 3.34525 11.7897 5.17282 8.86298C7.68288 4.84332 11.6154 1.917 16.1866 0.66717C20.7578 -0.582655 25.6321 -0.0642086 29.8382 2.11919C34.0442 4.3026 37.2731 7.99063 38.8815 12.4483C40.4899 16.9061 40.3596 21.8061 38.5166 26.1721C36.6736 30.538 33.2533 34.0493 28.9371 36.0061C24.621 37.9629 19.726 38.2216 15.2277 36.7306C15.2277 36.7306 13.6015 36.0441 14.1091 34.5212C14.6168 32.9982 21.2034 33.7265 21.2034 33.7265Z" v-bind:fill="selectedElement === 'history' ? '#FDFCFC' : '#38342E'"/>
            <path d="M6.09435 16.0347C6.52977 15.2054 7.55502 14.8862 8.38429 15.3216C9.21357 15.757 9.53285 16.7823 9.09743 17.6115L6.29421 22.9503C5.85878 23.7796 4.83354 24.0989 4.00426 23.6635C3.17499 23.228 2.85571 22.2028 3.29113 21.3735L6.09435 16.0347Z" v-bind:fill="selectedElement === 'history' ? '#FDFCFC' : '#38342E'"/>
            <path d="M0.217815 17.7556C-0.241102 16.9391 0.0487836 15.9051 0.865294 15.4462C1.6818 14.9873 2.71574 15.2772 3.17466 16.0937L6.12913 21.3503C6.58804 22.1668 6.29816 23.2008 5.48165 23.6597C4.66514 24.1186 3.6312 23.8287 3.17228 23.0122L0.217815 17.7556Z" v-bind:fill="selectedElement === 'history' ? '#FDFCFC' : '#38342E'"/>
          </svg>
          <label>История</label>
        </router-link>
      </li>
      <li
        v-bind:class="reportsClass"
        v-on:mouseenter.passive="openMenu('reports')"
        v-on:mouseleave.passive="isOverReports = false"
      >
        <svg class="main-menu-icon" viewBox="0 0 30 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7.584 11.5C7.584 10.6716 8.25557 10 9.084 10H20.9723C21.8008 10 22.4723 10.6716 22.4723 11.5C22.4723 12.3284 21.8008 13 20.9723 13H9.084C8.25557 13 7.584 12.3284 7.584 11.5Z" v-bind:fill="selectedElement === 'reports' ? '#FDFCFC' : '#38342E'"/>
          <path d="M9.084 16C8.25557 16 7.584 16.6716 7.584 17.5C7.584 18.3284 8.25557 19 9.084 19H20.9723C21.8008 19 22.4723 18.3284 22.4723 17.5C22.4723 16.6716 21.8008 16 20.9723 16H9.084Z" v-bind:fill="selectedElement === 'reports' ? '#FDFCFC' : '#38342E'"/>
          <path d="M7.584 23.5C7.584 22.6716 8.25557 22 9.084 22H20.9723C21.8008 22 22.4723 22.6716 22.4723 23.5C22.4723 24.3284 21.8008 25 20.9723 25H9.084C8.25557 25 7.584 24.3284 7.584 23.5Z" v-bind:fill="selectedElement === 'reports' ? '#FDFCFC' : '#38342E'"/>
          <path d="M9.084 28C8.25557 28 7.584 28.6716 7.584 29.5C7.584 30.3284 8.25557 31 9.084 31H20.9723C21.8008 31 22.4723 30.3284 22.4723 29.5C22.4723 28.6716 21.8008 28 20.9723 28H9.084Z" v-bind:fill="selectedElement === 'reports' ? '#FDFCFC' : '#38342E'"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M5.95533 0C2.66629 0 0 2.75517 0 6.15385V33.8462C0 37.2448 2.66629 40 5.95533 40H23.8213C27.1104 40 30 37.9554 30 34.5567V6C30 2.60132 27.1104 0 23.8213 0H5.95533ZM23.7097 3H5.56452C4.33113 3 2.90323 4.7255 2.90323 6V34.5567C2.90323 35.8312 4.08919 37 5.32258 37H23.7097C24.9431 37 27.0968 35.7745 27.0968 34.5V6C27.0968 4.7255 24.9431 3 23.7097 3Z" v-bind:fill="selectedElement === 'reports' ? '#FDFCFC' : '#38342E'"/>
        </svg>
        <label>Отчёты</label>
      </li>
      <li
        v-bind:class="adminClass"
        v-on:mouseenter.passive="openMenu('admin')"
        v-on:mouseleave.passive="isOverAdmin = false"
      >
        <svg class="main-menu-icon" viewBox="0 0 39 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M15.8605 0.000916544C15.8252 -4.58791e-05 15.7899 -0.000250263 15.7546 0.000303043C15.7028 -0.000509942 15.6509 0.000312842 15.599 0.0027714C15.5226 0.00639501 15.4466 0.0153202 15.3715 0.0294827C14.9113 0.116205 14.4865 0.331734 14.1452 0.649237C13.808 0.962833 13.566 1.36303 13.4433 1.80377L12.2876 5.81626C11.6168 6.15169 10.9829 6.53386 10.382 6.95065L6.39835 5.94375C5.87186 5.80563 5.31501 5.8455 4.81378 6.05663C4.30859 6.26942 3.89051 6.64312 3.62141 7.11632C3.62102 7.117 3.62063 7.11769 3.62025 7.11837L0.322345 12.9012C0.319141 12.9069 0.31597 12.9125 0.312832 12.9182C0.0539981 13.3847 -0.0478188 13.9216 0.0208605 14.4493C0.089535 14.977 0.325533 15.4709 0.697179 15.8562L3.52658 18.7822C3.48641 19.1623 3.45669 19.5711 3.45669 20.0005C3.45669 20.4298 3.48641 20.8386 3.52658 21.2186L0.697121 24.1448C0.325547 24.53 0.0895705 25.0239 0.0208941 25.5515C-0.0477771 26.0792 0.0539731 26.616 0.312774 27.0826C0.315931 27.0883 0.319121 27.0939 0.322345 27.0996L3.62017 32.8823C3.62045 32.8828 3.62074 32.8833 3.62102 32.8838C3.89006 33.3573 4.30823 33.7313 4.81364 33.9442C5.31509 34.1555 5.87199 34.1952 6.39831 34.0571L10.382 33.0502C10.9829 33.467 11.6168 33.8492 12.2876 34.1846L13.4467 38.2089C13.5963 38.725 13.9094 39.1809 14.3419 39.5054C14.7725 39.8283 15.2974 40.0028 15.8377 40H22.4255C22.9659 40.0028 23.4907 39.8283 23.9213 39.5054C24.3539 39.1809 24.6669 38.725 24.8165 38.2089L25.9756 34.1846C26.6465 33.8492 27.2803 33.467 27.8812 33.0502L31.8649 34.0572C32.3913 34.1952 32.9481 34.1555 33.4496 33.9442C33.9551 33.7312 34.3734 33.3571 34.6424 32.8835C34.6426 32.8831 34.6428 32.8827 34.6431 32.8823L37.9409 27.0996C37.9441 27.0939 37.9473 27.0883 37.9505 27.0826C38.2093 26.616 38.311 26.0792 38.2423 25.5515C38.1737 25.0239 37.9377 24.53 37.5661 24.1448L34.7367 21.2186C34.7768 20.8386 34.8065 20.4298 34.8065 20.0005C34.8065 19.5711 34.7768 19.1623 34.7366 18.7822L37.566 15.8562C37.9377 15.4709 38.1737 14.977 38.2424 14.4493C38.3111 13.9215 38.2092 13.3847 37.9504 12.9182C37.9473 12.9125 37.9441 12.9069 37.9409 12.9012L34.643 7.11837C34.6428 7.11801 34.6426 7.11766 34.6424 7.11731C34.3733 6.64367 33.955 6.26958 33.4495 6.05663C32.9482 5.8455 32.3914 5.80563 31.8649 5.94374L27.8813 6.95065C27.2803 6.53386 26.6464 6.15169 25.9756 5.81626L24.8165 1.79192C24.6669 1.27594 24.3539 0.820015 23.9212 0.495482C23.4909 0.172663 22.9661 -0.00192348 22.4258 0.000916544H15.8605ZM16.4483 3.30367H21.8149L23.0098 7.45221C23.1466 7.92701 23.4888 8.31563 23.9424 8.51138C24.859 8.90686 25.7162 9.42972 26.5329 10.0536C26.9334 10.3595 27.4516 10.4659 27.9401 10.3424L32.0824 9.29538L34.7659 14.0008L31.8134 17.0542C31.4617 17.4178 31.2962 17.9225 31.3641 18.4237C31.4436 19.0111 31.5038 19.4979 31.5038 20.0005C31.5038 20.503 31.4436 20.9897 31.3641 21.577C31.2962 22.0783 31.4617 22.583 31.8133 22.9466L34.7658 26.0001L32.0824 30.7055L27.9401 29.6585C27.4516 29.535 26.9334 29.6413 26.533 29.9472C25.7162 30.5711 24.8589 31.0941 23.9425 31.4895C23.4888 31.6852 23.1466 32.0739 23.0098 32.5487L21.8149 36.6972H16.4483L15.2534 32.5487C15.1166 32.0739 14.7744 31.6852 14.3207 31.4895C13.4043 31.0941 12.5471 30.5711 11.7302 29.9472C11.3298 29.6413 10.8116 29.535 10.3231 29.6585L6.18083 30.7055L3.49738 26.0001L6.44989 22.9466C6.8015 22.583 6.96706 22.0783 6.89916 21.577C6.8196 20.9897 6.75944 20.503 6.75944 20.0005C6.75944 19.4979 6.81961 19.0111 6.89916 18.4238C6.96706 17.9225 6.80149 17.4178 6.44988 17.0542L3.49737 14.0008L6.1808 9.29538L10.3231 10.3424C10.8117 10.4659 11.3299 10.3595 11.7303 10.0536C12.547 9.42972 13.4043 8.90686 14.3208 8.51138C14.7745 8.31563 15.1167 7.92701 15.2534 7.45221L16.4483 3.30367Z" v-bind:fill="selectedElement === 'admin' ? '#FDFCFC' : '#38342E'"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M19.0826 23.3027C20.9066 23.3027 22.3853 21.8241 22.3853 20C22.3853 18.1759 20.9066 16.6972 19.0826 16.6972C17.2585 16.6972 15.7798 18.1759 15.7798 20C15.7798 21.8241 17.2585 23.3027 19.0826 23.3027ZM19.0826 26.6055C22.7307 26.6055 25.6881 23.6481 25.6881 20C25.6881 16.3519 22.7307 13.3945 19.0826 13.3945C15.4345 13.3945 12.4771 16.3519 12.4771 20C12.4771 23.6481 15.4345 26.6055 19.0826 26.6055Z" v-bind:fill="selectedElement === 'admin' ? '#FDFCFC' : '#38342E'"/>
        </svg>
        <label>Админка</label>
      </li>
      <li class="with-submenu logout show-for-large" @click="logout">
        <svg class="main-menu-icon" viewBox="0 0 35 41" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M27.6499 15.5398C28.3715 14.8104 29.5415 14.8104 30.2631 15.5398L33.9588 19.2751C34.6804 20.0045 34.6804 21.1871 33.9588 21.9164L30.2631 25.6518C29.5415 26.3812 28.3715 26.3812 27.6499 25.6518C26.9283 24.9224 26.9283 23.7399 27.6499 23.0105L30.039 20.5958L27.6499 18.1811C26.9283 17.4517 26.9283 16.2691 27.6499 15.5398Z" fill="#38342E"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M15.6522 20.5958C15.6522 19.5643 16.4795 18.7281 17.5 18.7281H30.8043C31.8249 18.7281 32.6522 19.5643 32.6522 20.5958C32.6522 21.6273 31.8249 22.4635 30.8043 22.4635H17.5C16.4795 22.4635 15.6522 21.6273 15.6522 20.5958Z" fill="#38342E"/>
          <path fill-rule="evenodd" clip-rule="evenodd" d="M10.9754 6.42773C7.36164 8.79587 4.19565 12.5554 4.19565 20.9693C4.19565 29.3907 7.26591 32.6137 10.7289 34.5583C14.3807 36.6088 18.8998 36.6552 22.1003 36.2958C23.1146 36.1818 24.0282 36.9206 24.1409 37.9458C24.2536 38.971 23.5227 39.8944 22.5084 40.0083C19.0567 40.3959 13.5976 40.4422 8.93414 37.8236C4.08191 35.0989 0.5 30.4777 0.5 20.9693C0.5 11.4536 4.17097 6.43501 8.96486 3.29348C13.6327 0.234532 19.1159 -0.17273 22.6255 0.453269C23.6305 0.632528 24.3014 1.60131 24.1241 2.61711C23.9467 3.6329 22.9882 4.31105 21.9832 4.13179C19.2102 3.63718 14.7151 3.977 10.9754 6.42773Z" fill="#38342E"/>
        </svg>
        <label>Выйти</label>
      </li>
    </ul>
  </nav>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Menu',
  props: ['selectedElement'],
  data () {
    return {
      adminSubmenuShown: false,
      reportsSubmenuShown: false,
      isOverAdmin: false,
      isOverReports: false,
      isOverNoSubmenuEl: false,
      isOverMenu: false
    }
  },
  methods: {
    openMenu: function (menu) {
      if (menu === 'admin') {
        this.isOverAdmin = true
        setTimeout(() => {
          if (this.isOverAdmin && !this.isOverNoSubmenuEl && this.isOverMenu) {
            this.adminSubmenuShown = true
            this.reportsSubmenuShown = false
          }
        }, 100)
      }
      if (menu === 'reports') {
        this.isOverReports = true
        setTimeout(() => {
          if (this.isOverReports && !this.isOverNoSubmenuEl && this.isOverMenu) {
            this.adminSubmenuShown = false
            this.reportsSubmenuShown = true
          }
        }, 100)
      }
    },
    closeMenus: function (force) {
      if (this.isOverNoSubmenuEl || !this.isOverMenu || force) {
        this.reportsSubmenuShown = false
        this.adminSubmenuShown = false
      }
    },
    leaveMenu: function () {
      this.isOverMenu = false
      setTimeout(this.closeMenus, 300)
    },
    enterNoSubmenuEl: function () {
      this.isOverNoSubmenuEl = true
      setTimeout(this.closeMenus, 300)
    },
    logout: function () {
      axios.post(`/logout`)
        .then(response => {
          window.location.href = '/login'
        })
    }
  },
  computed: {
    navClass: function () {
      var navClass = 'main-menu'
      if (this.adminSubmenuShown || this.reportsSubmenuShown) {
        navClass += ' submenu-shown'
      }
      return navClass
    },
    adminClass: function () {
      var adminClass = 'with-submenu'
      if (this.selectedElement === 'admin') {
        adminClass += ' selected'
      }
      if (this.adminSubmenuShown) {
        adminClass += ' hovered'
      }
      return adminClass
    },
    reportsClass: function () {
      var reportsClass = 'with-submenu'
      if (this.selectedElement === 'reports') {
        reportsClass += ' selected'
      }
      if (this.reportsSubmenuShown) {
        reportsClass += ' hovered'
      }
      return reportsClass
    }
  }
}
</script>

<style>
</style>
