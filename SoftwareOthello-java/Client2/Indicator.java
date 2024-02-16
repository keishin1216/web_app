import java.awt.*;
import javax.swing.*;

public class Indicator extends JPanel{
    JLabel text;
    int fontSize;
    String tempText;

    Indicator() {
        tempText = "";

        text = new JLabel();
        fontSize = 20;
        text.setFont(new Font(Font.DIALOG, Font.PLAIN, fontSize));
        text.setSize(text.getPreferredSize());
        text.setForeground(Color.BLUE);
        add(text);
    }

    public void displayText(String text) {
        tempText = text;
        this.text.setText(text);
    }

    // 以前displayTextで呼び出したtextに新たなtextを連結して表示
    public void displayLinkedText(String text) {
        this.text.setText(tempText + text);
    }

}
