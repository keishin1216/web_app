import java.io.*;
import java.net.*;

class Player {
    String name="Null";
    char piece;
    boolean isAvailable;//打てる場所が無いときにfalseになる。
    static boolean isWhite = true;
    Player() {
        //System.out.print("あなたの名前を入力してください：");
        //BufferedReader reader = new BufferedReader(new  InputStreamReader(System.in));
        try {
            //this.name = reader.readLine();
            this.isAvailable = true;
            if (isWhite) {
                this.piece = 'W';
                isWhite = false;
            } else {
                this.piece = 'B';
                isWhite = true;
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    @Override
    public String toString() {
        return "name: " + this.name + "; piece: " + piece + ";";
    }
}

class ManageBoard extends Thread{
    Player playerMe, playerYou;
    GameWindow window;
    char[][] board = new char[8][8];
    int countW=2, countB=2;
    int[][] Directions = {
        {0,-1},{1,-1},{1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1}
    }; //int[8][2];オセロ盤での探索に必要な8方向を表す。
    boolean isStop=false;

    ManageBoard(Player playerMe, Player playerYou) {
        this.playerMe=playerMe;
        this.playerYou=playerYou;
        this.playerMe.name = "あなた";
        this.playerYou.name = "相手";
        for(int i=0; i<8; i++) {
            for(int j=0; j<8; j++) {
                board[i][j] = 'E';
            }
        }
        for(int i=2; i<6; i++) {
            for(int j=2; j<6; j++) {
                board[i][j] = '*';
            }
        }
        board[3][3] = 'W';
        board[4][4] = 'W';
        board[3][4] = 'B';
        board[4][3] = 'B';

        countB = 2; countW = 2;
        countB = 2; countW = 2;

        window = new GameWindow("OthelloServer Game", this);
        window.isAbleToClick = true;
    }

    void ShowBoard() {
        System.out.print(' ');
        for(int i=0; i<8; i++) {
            System.out.print((char)('a'+i));
        }
        System.out.println();
        for(int i=0; i<8; i++) {
            System.out.print(i+1);
            for(int j=0; j<8; j++) {
                System.out.print(board[i][j]);
            }
            System.out.println();
        }
        System.out.println("Wの個数: "+countW+" Bの個数:"+countB);
        System.out.println();
    }
 
    void Stop() {
        try {
            while (isStop) {
                Thread.sleep(100);
            }
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    char ReturnAnotherPiece(char piece){//対戦相手の駒の色を返す関数
        if (piece == 'W') return 'B';
        else return 'W';
    }

    boolean IsIncluded(int y,int x){//引数の座標が盤内に入っているか確認してboolean型で返す。
        if (0<=y&&y<=7&&0<=x&&x<=7) return true;
        else return false;
    }

    void ReverseOnePiece(char piece, int y, int x) {//Board[y][x]の駒を1枚ひっくり返し、駒の個数を更新する。
        if (piece == 'W') {
            board[y][x] = 'W';
            window.board.placePiece();
            countW++;countB--;
        } else {
            board[y][x] = 'B';
            window.board.placePiece();
            countB++;countW--;
        }
    }

    boolean ExploreOneDirection(char piece, int y, int x, int[] onedirection) {//そこに駒をおいて相手の駒をひっくり返せるのか？をboolean型で返す。ただし8方向のうち1方向しか確かめない。
        char anotherpiece = ReturnAnotherPiece(piece);
        boolean isAnotherPiece=false, isYourPiece=false;//isAnotherPieceは相手の駒が打った場所の隣にあったらTrue,isYourPieceは探索した方向に自分の駒があったらTrueになる。
        y+=onedirection[0];x+=onedirection[1];
        if (IsIncluded(y, x) && board[y][x]==anotherpiece) isAnotherPiece = true;
        while (IsIncluded(y, x)) {
            if (board[y][x]==piece) isYourPiece = true;
            else if (board[y][x]=='*' || board[y][x]=='E') break;//例えば"*WW*B"みたいな配置だった場合、左端にBを入れてもひっくり返せないので,4番目の"*"でbreakを入れてisYourPiece=falseのままにする。
            y+=onedirection[0];x+=onedirection[1];
        }
        if (isAnotherPiece&&isYourPiece) return true;
        else return false;
    }

    void PlaceandReversethePiece(char piece, int y, int x, int[] onedirection) {//１方向のみ駒をひっくり返す。ExploreOneDirectionがTrueを返した方向のみにこのメソッドを適応する。
        board[y][x]=piece;
        window.board.placePiece();
        y+=onedirection[0];x+=onedirection[1];
        while (true) {
            if (board[y][x]==piece) break;
            else ReverseOnePiece(piece, y, x);
            y+=onedirection[0];x+=onedirection[1];
        }//自分の駒が出てくるまで盤上の駒をReverseOnePiece(piece, y, x)でひっくり返す。
    }

    boolean IsAbletoHit(Player player, int y, int x) {//そのマスに駒を打てるかどうかをbooleanで返す。
        if (board[y][x]=='*') {
            for (int i = 0; i < 8; i++) {
                if (ExploreOneDirection(player.piece, y, x, Directions[i])) return true;//もしそのマスが"*"で、なおかつ8方向のうち1方向でも駒をひっくり返せるならTrueを返す。
            }
            return false;
        } else {
            return false;
        }
    }

    boolean IsSkipped(Player player) {//手版をスキップするかどうかbooleanで返す。スキップするときtrueを返すことに注意。
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (IsAbletoHit(player, i, j)) {
                    player.isAvailable = true;
                    return false;
                }
            }
        }
        player.isAvailable = false;
        return true;
    }

    void HitPiece(Player player, int y, int x) {//playerが駒を(y,x)に打つ。
        for (int i = 0; i < 8; i++) {
            int yd = y + Directions[i][0], xd = x + Directions[i][1];
            if (IsIncluded(yd, xd) && board[yd][xd]=='E') board[yd][xd] = '*';//IsIncluded(yd, xd)を先に置かないとエラーがおこる事に注意。盤面の外を参照しないように"*"をおく
        }//まず、打った周りに駒に隣接することを意味する"*"をおく
        for (int i = 0; i < 8; i++) {
            if (ExploreOneDirection(player.piece, y, x, Directions[i])) PlaceandReversethePiece(player.piece, y, x, Directions[i]);;
        }//次に、8方向に対して1方向ずつひっくり返せるかどうか確認して、ひっくり返せるならPlaceandReversethePiece(player.piece, y, x, Directions[i])で実際にひっくり返す。
        if (board[y][x]=='W')  countW++;//最後に、駒を打ったことで盤上の駒が1つ増えるので、それを数える。
        else countB++;
    }

    void WaitGUIclick(Player player) {
        System.out.println("あなたの駒は"+player.piece+"です。");
        System.out.println("どこに打ちますか？クリックしてください:");
        window.isAbleToClick = true;//新しく入れた。
        
        // ここでGUI側の入力待ちに入る
    }

    void checkBoard(int x, int y) {
        if (IsAbletoHit(playerMe, y-1, x-'a')) {
            char a = (char) (y+'0');
            char b = (char) ('0'+x-'0');
            char[] c = new char[] {a, b};
            String Locate = new String(c);
            System.out.println(Locate);//確認のため
            String tmp = "";
            try {
                while (true) {
                    OthelloServer.out.println(Locate);//送信！
                    OthelloServer.out.println("OK");//送信！
                    tmp = OthelloServer.in.readLine();
                    if (tmp.equals("OK")) break;
                }
            } catch (Exception e) {
                //TODO: handle exception
            }
            HitPiece(playerMe, y-1, x-'a');
            window.isAbleToClick = false;//新しく入れた。
            isStop = false;//新しく入れた。
        } else {
            System.out.println("その場所には打てません。");
            window.isAbleToClick = false;//新しく入れた。
            //isStop = false;//新しく入れた。
            WaitGUIclick(playerMe);
        }
    }

    void DisplayV(char piece, Player playerServer, Player playerMe) {
        String winner;
        if (playerServer.piece==piece) winner = playerServer.name;
        else winner = playerMe.name;
        System.out.println(winner+"さんの勝利！");
        window.isAbleToClick = false;
    }
    void WhichisV(Player playerServer, Player playerMe) {//どっちが勝ったか判断して表示する。
        if (countB>countW) DisplayV('B', playerServer, playerMe);
        else if (countW>countB) DisplayV('W', playerServer, playerMe);
        else {
            System.out.println("引き分けです。");
            window.isAbleToClick = false;
        }
    }

    void ReadIn(Player player) {//通信のため新しく追加したメソッド。相手の手を解釈する。
        try {
            System.out.println("相手の入力待ちです。");
            window.isAbleToClick = false;
            String tmp = "";
            String str = "";
            while (true) {
                tmp = OthelloServer.in.readLine();
                if (tmp.equals("OK")) break;
                str = tmp;
            }
            OthelloServer.out.println("OK");//送信！
            int y = str.charAt(0)-'1';
            int x =str.charAt(1)-'a';
            HitPiece(player, y, x);
            System.out.println("相手の手："+str);
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    void PlayerTurn (Player player) {//番が来たプレイヤーに対して盤面を表示し、打てる場所があればScanandHitPieceメソッドを実行する。打てる場所が無ければスキップする。
        ShowBoard();
        if (IsSkipped(player)) {
            System.out.println(player.name + "さんの打てる場所がありません。スキップします。");
        } else {
            if (player == playerMe) {
                System.out.println(player.name + "さんの番です。");
                WaitGUIclick(player);
                isStop = true;//新しく入れた。
                Stop();//新しく入れた。
            } else {
                System.out.println("相手の番です。");
                ReadIn(player);
            }
        }
    }

    void Playgame(Player player1, Player player2) {//2人とも駒が打てなくなるまでそれぞれのプレイヤーに手番を回す。打てなくなったらどっちが勝っているか判定する。
        while (player1.isAvailable||player2.isAvailable) {
            PlayerTurn(player1);
            PlayerTurn(player2);
        }
        WhichisV(player1,player2);
    }
    public void run() {//2人とも駒が打てなくなるまでそれぞれのプレイヤーに手番を回す。打てなくなったらどっちが勝っているか判定する。
        Playgame(playerMe, playerYou);//前に来る人が先手。サーバ化クライアント化でちがうことにちゅうい。
    }
    
}

public class OthelloServer {
    public static int PORT = 8080; //ポート番号を設定する
    static BufferedReader in;
    static PrintWriter out;
    static boolean flag=true;
    public static void main(String[] args) 
    throws IOException {
        ServerSocket s = new ServerSocket(PORT); // ソケットを作成する
        System.out.println("Started: " + s);
        try {
            Socket socket = s.accept(); // コネクション設定要求を待つ
            try {
                System.out.println("Connection accepted: " + socket);
                in = new BufferedReader(new InputStreamReader(socket.getInputStream())); // データ受信用バッファの設定
                out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true); // 送信バッファ設定
                
                // 打った場所の送受信
                
                //while (true) {
                    //String str = in.readLine(); // データの受信
                    //if(str.equals("END")) break;
                    //System.out.println("Echoing : ");
                    //out.println(str); // データの送信
                //}
                Player playerMe = new Player();
                Player playerYou = new Player();
                ManageBoard board = new ManageBoard(playerMe, playerYou);

                board.start();
                
                try {
                    board.join();
                } catch (Exception e) {
                    //TODO: handle exception
                    e.printStackTrace();
                }
            } finally {
                System.out.println("closing...");
                socket.close();
            }
        } finally {
            s.close();
        }

        
    }
}
