import Vue from 'vue'
import Router from 'vue-router'
import Session from '@/components/pages/Session'
import EditSession from '@/components/pages/EditSession'
import SessionsHistory from '@/components/pages/SessionsHistory'
import EditService from '@/components/pages/EditService'
import EditGoodsSell from '@/components/pages/EditGoodsSell'
import EditEmployeePayment from '@/components/pages/EditEmployeePayment'
import EditExpense from '@/components/pages/EditExpense'
import EditClient from '@/components/pages/EditClient'
import Clients from '@/components/pages/Clients'
import UploadExpenses from '@/components/pages/UploadExpenses'
import Offices from '@/components/pages/Offices'
import EditOffice from '@/components/pages/EditOffice'
import ServiceTypes from '@/components/pages/ServiceTypes'
import EditServiceType from '@/components/pages/EditServiceType'
import GoodsTypes from '@/components/pages/GoodsTypes'
import EditGoodsType from '@/components/pages/EditGoodsType'
import ExpenseTypes from '@/components/pages/ExpenseTypes'
import EditExpenseType from '@/components/pages/EditExpenseType'
import EmployeePaymentTypes from '@/components/pages/EmployeePaymentTypes'
import EditEmployeePaymentType from '@/components/pages/EditEmployeePaymentType'
import Employees from '@/components/pages/Employees'
import EditEmployee from '@/components/pages/EditEmployee'
import MasterTypes from '@/components/pages/MasterTypes'
import EditMasterType from '@/components/pages/EditMasterType'
import EmployeesReport from '@/components/pages/EmployeesReport'
import ClientsReport from '@/components/pages/ClientsReport'
import FinancialReport from '@/components/pages/FinancialReport'
import NotFound from '@/components/pages/NotFound'

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
    },
    {
      path: '/EditSession/:id?',
      name: 'EditSession',
      component: EditSession,
      meta: {
        title: 'Смена'
      }
    },
    {
      path: '/SessionsHistory',
      name: 'SessionsHistory',
      component: SessionsHistory,
      meta: {
        title: 'История смен и операций'
      }
    },
    {
      path: '/EditService/:id?',
      name: 'EditService',
      component: EditService,
      meta: {
        title: 'Услуга'
      }
    },
    {
      path: '/EditGoodsSell/:id?',
      name: 'EditGoodsSell',
      component: EditGoodsSell,
      meta: {
        title: 'Продажа товаров'
      }
    },
    {
      path: '/EditEmployeePayment/:id?',
      name: 'EditEmployeePayment',
      component: EditEmployeePayment,
      meta: {
        title: 'Выплата сотруднику'
      }
    },
    {
      path: '/EditExpense/:id?',
      name: 'EditExpense',
      component: EditExpense,
      meta: {
        title: 'Расход'
      }
    },
    {
      path: '/EditClient/:id?',
      name: 'EditClient',
      component: EditClient,
      meta: {
        title: 'Клиент'
      }
    },
    {
      path: '/Clients',
      name: 'Clients',
      component: Clients,
      meta: {
        title: 'Клиенты'
      }
    },
    {
      path: '/UploadExpenses',
      name: 'UploadExpenses',
      component: UploadExpenses,
      meta: {
        title: 'Загрузка расходов'
      }
    },
    {
      path: '/Offices',
      name: 'Offices',
      component: Offices,
      meta: {
        title: 'Отделения'
      }
    },
    {
      path: '/EditOffice/:id?',
      name: 'EditOffice',
      component: EditOffice,
      meta: {
        title: 'Отделение'
      }
    },
    {
      path: '/ServiceTypes',
      name: 'ServiceTypes',
      component: ServiceTypes,
      meta: {
        title: 'Услуги'
      }
    },
    {
      path: '/EditServiceType/:id?',
      name: 'EditServiceType',
      component: EditServiceType,
      meta: {
        title: 'Тип услуги'
      }
    },
    {
      path: '/GoodsTypes',
      name: 'GoodsTypes',
      component: GoodsTypes,
      meta: {
        title: 'Товары'
      }
    },
    {
      path: '/EditGoodsType/:id?',
      name: 'EditGoodsType',
      component: EditGoodsType,
      meta: {
        title: 'Товар'
      }
    },
    {
      path: '/ExpenseTypes',
      name: 'ExpenseTypes',
      component: ExpenseTypes,
      meta: {
        title: 'Типы расходов'
      }
    },
    {
      path: '/EditExpenseType/:id?',
      name: 'EditExpenseType',
      component: EditExpenseType,
      meta: {
        title: 'Тип расхода'
      }
    },
    {
      path: '/EmployeePaymentTypes',
      name: 'EmployeePaymentTypes',
      component: EmployeePaymentTypes,
      meta: {
        title: 'Типы выплат сотруднику'
      }
    },
    {
      path: '/EditEmployeePaymentType/:id?',
      name: 'EditEmployeePaymentType',
      component: EditEmployeePaymentType,
      meta: {
        title: 'Тип выплаты сотруднику'
      }
    },
    {
      path: '/Employees',
      name: 'Employees',
      component: Employees,
      meta: {
        title: 'Сотрудники'
      }
    },
    {
      path: '/EditEmployee/:id?',
      name: 'EditEmployee',
      component: EditEmployee,
      meta: {
        title: 'Сотрудник'
      }
    },
    {
      path: '/MasterTypes',
      name: 'MasterTypes',
      component: MasterTypes,
      meta: {
        title: 'Категории мастеров'
      }
    },
    {
      path: '/EditMasterType/:id?',
      name: 'EditMasterType',
      component: EditMasterType,
      meta: {
        title: 'Категория мастера'
      }
    },
    {
      path: '/EmployeesReport',
      name: 'EmployeesReport',
      component: EmployeesReport,
      meta: {
        title: 'Отчёт по сотрудникам'
      }
    },
    {
      path: '/ClientsReport',
      name: 'ClientsReport',
      component: ClientsReport,
      meta: {
        title: 'Отчёт по клиентам'
      }
    },
    {
      path: '/FinancialReport',
      name: 'FinancialReport',
      component: FinancialReport,
      meta: {
        title: 'Финансовый отчёт'
      }
    },
    {
      path: '*',
      component: NotFound,
      meta: {
        title: 'Страница не найдена'
      }
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})
