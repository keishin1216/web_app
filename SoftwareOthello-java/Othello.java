import java.io.BufferedReader;
import java.io.InputStreamReader;

class Player {
    String name;
    char piece;
    boolean isAvailable;//打てる場所が無いときにfalseになる。
    static boolean isWhite = true;

    Player() {
        System.out.print("あなたの名前を入力してください：");
        BufferedReader reader = new BufferedReader(new  InputStreamReader(System.in));
        try {
            this.name = reader.readLine();
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

class ManageBoard {
    GameWindow window;
    Player player1, player2;
    Player playerNow;
    char[][] board = new char[8][8];
    int countW=2, countB=2;
    int[][] Directions = {
        {0,-1},{1,-1},{1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1}
    }; //int[8][2];オセロ盤での探索に必要な8方向を表す。

    ManageBoard(Player player1, Player player2) {
        this.player1 = player1;
        this.player2 = player2;

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

        window = new GameWindow("Othello Game", this);
        window.isAbleToClick = true;
        playerNow = player1;
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
        window.indicator.displayLinkedText("駒:"+player.piece+" 打つ場所を選択してください");
        System.out.println("あなたの駒は"+player.piece+"です。");
        System.out.println("どこに打ちますか？クリックしてください:");
        // ここでGUI側の入力待ちに入る
    }

    // GUIにクリック入力があるとこのメソッドが実行される
    void checkBoard(int x, int y) {
        if (IsAbletoHit(playerNow, y-1, x-'a')) {
            HitPiece(playerNow, y-1, x-'a');
            if(playerNow == player1) {
                playerNow = player2;
            } else {
                playerNow = player1;
            }
            Playgame();
        } else {
            window.indicator.displayText("その場所には打てません。");
            System.out.println("その場所には打てません。");
            WaitGUIclick(playerNow);
        }
    }

    void DisplayV(char piece, Player player1, Player player2) {
        String winner;
        if (player1.piece==piece) winner = player1.name;
        else winner = player2.name;
        window.indicator.displayText(winner+"さんの勝利！");
        System.out.println(winner+"さんの勝利！");
        window.isAbleToClick = false;
        //window.forceQuit();
    }
    void WhichisV(Player player1, Player player2) {//どっちが勝ったか判断して表示する。
        if (countB>countW) DisplayV('B', player1, player2);
        else if (countW>countB) DisplayV('W', player1, player2);
        else {
            window.indicator.displayText("引き分けです。");
            System.out.println("引き分けです。");
            window.isAbleToClick = false;
            //window.forceQuit();
        }
    }

    void PlayerTurn () {//番が来たプレイヤーに対して盤面を表示し、打てる場所があればWaitGUIclickメソッドを実行する。打てる場所が無ければスキップする。
        ShowBoard();
        if (IsSkipped(playerNow)) {
            window.indicator.displayText(playerNow.name + "さんの打てる場所がありません。スキップします。");
            System.out.println(playerNow.name + "さんの打てる場所がありません。スキップします。");
            if(playerNow == player1) {
                playerNow = player2;
            } else {
                playerNow = player1;
            }
            Playgame();
        } else {
            window.indicator.displayText(playerNow.name + "さんの番です。");
            System.out.println(playerNow.name + "さんの番です。");
            WaitGUIclick(playerNow);
        }
    }

    void Playgame() {//2人とも駒が打てなくなるまでそれぞれのプレイヤーに手番を回す。打てなくなったらどっちが勝っているか判定する。
        if(player1.isAvailable || player2.isAvailable) {
            PlayerTurn();
        } else {
            WhichisV(player1,player2);
        }
    }
}

public class Othello {
    public static void main(String[] args) {
        Player player1 = new Player();
        Player player2 = new Player();
        ManageBoard board = new ManageBoard(player1, player2);

        board.Playgame();
    }
}
