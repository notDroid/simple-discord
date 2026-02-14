import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { decodeJwt } from 'jose';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session_token')?.value

  // If user is on a protected path and has no token, kick them out
  if (!token && request.nextUrl.pathname.startsWith('/chats')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // If user is on login page but HAS a token, send them to chats
  if (token && request.nextUrl.pathname === '/login') {
    return NextResponse.redirect(new URL('/chats', request.url))
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/chats/:path*', '/login'],
}