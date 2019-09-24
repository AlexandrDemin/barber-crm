import Vue from 'vue'
import Router from 'vue-router'
import Session from '@/components/Session'
// import EditSession from '@/components/EditSession'
// import SessionsHistory from '@/components/SessionsHistory'
// import EditService from '@/components/EditService'
// import EditGoodsSell from '@/components/EditGoodsSell'
// import EditEmployeePayment from '@/components/EditEmployeePayment'
// import EditExpense from '@/components/EditExpense'
// import EditClient from '@/components/EditClient'
// import Clients from '@/components/Clients'
// import UploadExpenses from '@/components/UploadExpenses'
// import Offices from '@/components/Offices'
// import EditOffice from '@/components/EditOffice'
// import ServiceTypes from '@/components/ServiceTypes'
// import EditServiceType from '@/components/EditServiceType'
// import GoodsTypes from '@/components/GoodsTypes'
// import EditGoodsType from '@/components/EditGoodsType'
// import ExpenseTypes from '@/components/ExpenseTypes'
// import EditExpenseType from '@/components/EditExpenseType'
// import EmployeePaymentTypes from '@/components/EmployeePaymentTypes'
// import EditEmployeePaymentType from '@/components/EditEmployeePaymentType'
// import Employees from '@/components/Employees'
// import EditEmployee from '@/components/EditEmployee'
// import MasterTypes from '@/components/MasterTypes'
// import EditMasterType from '@/components/EditMasterType'
// import EmployeesReport from '@/components/EmployeesReport'
// import ClientsReport from '@/components/ClientsReport'
// import FinancialReport from '@/components/FinancialReport'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Session',
      component: Session,
      meta: {
        title: 'Смена'
      }
    }
  ]
})
