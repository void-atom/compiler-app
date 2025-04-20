int a=2;

int foo(int x, int y)
{
  a=3*x-4*y+a/2;
  return a;
}

int main()
{
  int x=foo(2,11);
  return x;
}