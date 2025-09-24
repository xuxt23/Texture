#include<cstdio>

int main(){
    int n,m,q;
    scanf("%d%d",&n,&m);
    
    // 使用数组而不是指针，更安全
    static int matrix[1005][1005];
    static int rowsum[1005][1005];
    
    // 读取矩阵
    for(int i=1;i<=n;++i){
        for(int j=1;j<=m;++j){
            scanf("%d",&matrix[i][j]);
        }
    }
    
    // 计算行前缀和
    for(int i=1;i<=n;++i){
        rowsum[i][0] = 0;
        for(int j=1;j<=m;++j){
            rowsum[i][j] = rowsum[i][j-1] + matrix[i][j];
        }
    }
    
    scanf("%d",&q);
    for(int i=1;i<=q;++i){
        int x,y,a,b;
        long long sum = 0;  // 使用long long防止溢出
        scanf("%d %d %d %d",&x,&y,&a,&b);
        
        // 计算从(x,y)开始，大小为a×b的子矩阵和
        for(int j=0;j<a;++j){
            sum += rowsum[x+j][y+b-1] - rowsum[x+j][y-1];
        }
        printf("%lld\n",sum);
    }
    return 0;
}