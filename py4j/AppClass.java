package py4j;



import java.util.ArrayList;



public class AppClass

{

    public int send_python_obj_to_java(app_1 e)

    {

        return 0;

    }



    public int fill_data_for_speech_request(ArrayList<Object> a)

    {

        return 0;

    }

    public int update_new_words_cloud(ArrayList<Object> b)

    {

        return 0;

    }

    public int process_user_actions(ArrayList<Object> c)

    {

        return 0;

    }

     public static void main(String[] args) {

        GatewayServer gatewayServer = new GatewayServer();

        GatewayServer.turnLoggingOff();

        gatewayServer.start();

        System.out.println("Gateway Server Started");

    }



}