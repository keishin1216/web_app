import javax.swing.*;
import javax.swing.event.MouseInputAdapter;
import java.awt.event.MouseEvent;

public class GameWindow extends JFrame {
    BoardPanel board;
    Indicator indicator;
    boolean isAbleToClick;      // ゲーム終了時はクリック入力を拒否する
    ManageBoard boardManager;
    int x, y;                   // ウィンドウ内におけるクリック位置の座標

    GameWindow(String title, ManageBoard boardManager) {
        this.boardManager = boardManager;
        indicator = new Indicator();
        isAbleToClick = false;

        // マスターフレーム設定
        setTitle(title);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);

        // 盤面フレーム設定
        board = new BoardPanel(560, 560+indicator.fontSize+5, boardManager);
        //getContentPane().setLayout(new FlowLayout());
        setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
        board.addMouseListener(new MouseCheck());
        getContentPane().add(board);

        // 文字列表示フレーム設定
        getContentPane().add(indicator);

        pack();
    }

    public void forceQuit() {
        dispose();
    }

    // 盤面のクリックイベント処理
    private class MouseCheck extends MouseInputAdapter {
        @Override
        public void mousePressed(MouseEvent e) {
            if(isAbleToClick) {
                x = e.getX();
                y = e.getY();
                // ウィンドウのうちオセロ盤面上の部分がクリックされた場合
                if(x>=board.xLowerLimit && x<=board.xUpperLimit && y>=board.yLowerLimit && y<=board.yUpperLimit) {
                    board.getPosition(x, y);
                    boardManager.checkBoard(board.xValue, board.yValue);
                }
            }
        }
    }
}

