'use client'

import { useActionState } from 'react'
import { loginAction } from '@/features/auth/actions'

export default function LoginPage() {
  const [state, action, isPending] = useActionState(loginAction, null)

  return (
    <div className="flex h-screen items-center justify-center bg-app-bg">
      <form action={action} className="flex flex-col gap-4 p-8 bg-white shadow-md rounded">
        <h1 className="text-xl font-bold">Sign In</h1>
        
        <input name="email" type="email" placeholder="Email" required className="border p-2" />
        <input name="password" type="password" placeholder="Password" required className="border p-2" />
        
        {state?.error && <p className="text-red-500 text-sm">{state.error}</p>}
        
        <button disabled={isPending} className="bg-brand text-white p-2 rounded">
          {isPending ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  )
}