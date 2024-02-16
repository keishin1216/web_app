import java.awt.*;
import javax.swing.*;

public class BoardPanel extends JPanel {
    ManageBoard boardManager;
    Graphics g;
    int width;              // 盤面表示フレームの幅
    int height;             // 盤面表示フレームの高さ
    int squareSize;         // 盤面のマス目の一辺の長さ
    int xLowerLimit;        // 盤面の左端の座標
    int xUpperLimit;        // 盤面の右端の座標
    int yLowerLimit;        // 盤面の上端の座標
    int yUpperLimit;        // 盤面の下端の座標
    int xValue;             // x座標を変換して得たクリック位置
    int yValue;             // y座標を変換して得たクリック位置
    int r;                  // 石の直径
    final static int d = 2; // 座標の微妙な位置調整

    BoardPanel(int width, int height, ManageBoard boardManager) {
        setPreferredSize(new Dimension(width, height));
        setCursor(new Cursor(Cursor.HAND_CURSOR));

        this.width = width;
        this.height = height;
        this.boardManager = boardManager;
        g = this.getGraphics();
        squareSize = 70;
        xLowerLimit = 0;
        xUpperLimit = xLowerLimit + squareSize*8;
        yLowerLimit = 0;
        yUpperLimit = yLowerLimit + squareSize*8;
        r = squareSize - 5;
    }

    @Override
    public void paintComponent(Graphics g) {
        // 最背面の背景
        g.setColor(Color.black);
        g.fillRect(0, 0, width, height);

        // 盤面の背景
        g.setColor(new Color(0, 170, 85));  // 緑色
        g.fillRect(xLowerLimit, yLowerLimit, xUpperLimit-xLowerLimit, yUpperLimit-yLowerLimit);

        // 4箇所に点を打つ
        g.setColor(Color.black);
        g.fillRect(xLowerLimit+squareSize*2-d, yLowerLimit+squareSize*2-d, 5, 5);
        g.fillRect(xLowerLimit+squareSize*2-d, yLowerLimit+squareSize*6-d, 5, 5);
        g.fillRect(xLowerLimit+squareSize*6-d, yLowerLimit+squareSize*2-d, 5, 5);
        g.fillRect(xLowerLimit+squareSize*6-d, yLowerLimit+squareSize*6-d, 5, 5);

        // 罫線描画
        g.setColor(Color.black);
        for(int i=0; i<9; i++) {
            g.drawLine(xLowerLimit, yLowerLimit+squareSize*i, xUpperLimit, yLowerLimit+squareSize*i);   // 横線
            g.drawLine(xLowerLimit+squareSize*i, yLowerLimit, xLowerLimit+squareSize*i, yUpperLimit);   // 縦線
        }

        // 石の配置
        for(int i=0; i<8; i++) {
            for(int j=0; j<8; j++) {
                if(boardManager.board[i][j] == '*') {
                    // 石を打つ候補地に薄く色付け
                    g.setColor(new Color(255, 222, 173, 85));
                    g.fillRect(xLowerLimit+j*squareSize+d, yLowerLimit+i*squareSize+d, squareSize-2*d, squareSize-2*d);
                } else if(boardManager.board[i][j] == 'W') {
                    g.setColor(Color.white);
                    g.fillOval(xLowerLimit+j*squareSize+d, yLowerLimit+i*squareSize+d, r, r);
                } else if(boardManager.board[i][j] == 'B') {
                    g.setColor(Color.black);
                    g.fillOval(xLowerLimit+j*squareSize+d, yLowerLimit+i*squareSize+d, r, r);
                }
            }
        }
    }

    // クリックした座標を8×8マスの位置に変換
    public void getPosition(int x, int y) {
        // クリックされたマスの列番号をチェック
        for(int i=xLowerLimit,count=0; i<=xUpperLimit; i+=squareSize,count++) {
            if(x>=i && x<i+squareSize) {
                xValue = 'a' + count;  // 'a'から'h'までのアルファベットを割り振る
            }
        }
        // クリックされたマスの行番号をチェック
        for(int i=yLowerLimit,count=1; i<=yUpperLimit; i+=squareSize,count++) {
            if(y>=i && y<i+squareSize) {
                yValue = count;   // 1から8までの数字を割り振る
            }
        }
    }

    // xValue, yValueの位置に石を置く
    public void placePiece() {
        repaint();
    }
}
