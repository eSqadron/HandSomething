using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;

public class TCPTestServer : MonoBehaviour
{
	#region private members 	
	/// <summary> 	
	/// TCPListener to listen for incomming TCP connection 	
	/// requests. 	
	/// </summary> 	
	private TcpListener tcpListener;
	/// <summary> 
	/// Background thread for TcpServer workload. 	
	/// </summary> 	
	private Thread tcpListenerThread;
	/// <summary> 	
	/// Create handle to connected tcp client. 	
	/// </summary> 	
	private TcpClient connectedTcpClient;
	#endregion

	public GameObject hand_prefab;
	master hand_object;
	public string[] splitArray;
	bool isTHere = false;

	// Use this for initialization
	void Start()
	{
		// Start TcpServer background thread 		
		tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
		tcpListenerThread.IsBackground = true;
		tcpListenerThread.Start();
		hand_object = Instantiate(hand_prefab, new Vector3(0, 0, 0), Quaternion.identity).GetComponent<master>();
		hand_object.start_spheres();
	}

	// Update is called once per frame
	void Update()
	{
		if (isTHere)
		{
			for (int i = 0; i < 21; i++)
			{
				hand_object.spheres[i].transform.position = new Vector3(float.Parse(splitArray[i * 3]) / 1000.0f
					, float.Parse(splitArray[i * 3 + 1]) / 1000.0f, float.Parse(splitArray[i * 3 + 2]) / 1000.0f);

			}
			if (hand_object.spheres[8].transform.position.y < hand_object.spheres[7].transform.position.y)
			{
				hand_object.set_color(8, Color.blue);
				hand_object.set_color(7, Color.blue);
				hand_object.set_color(6, Color.blue);
				hand_object.set_color(5, Color.blue);
			}
			else
			{
				hand_object.set_color(8, Color.white);
				hand_object.set_color(7, Color.white);
				hand_object.set_color(6, Color.white);
				hand_object.set_color(5, Color.white);
			}

			if (hand_object.spheres[12].transform.position.y < hand_object.spheres[11].transform.position.y)
			{
				hand_object.set_color(12, Color.blue);
				hand_object.set_color(11, Color.blue);
				hand_object.set_color(10, Color.blue);
				hand_object.set_color(9, Color.blue);
			}
			else
			{
				hand_object.set_color(12, Color.white);
				hand_object.set_color(11, Color.white);
				hand_object.set_color(10, Color.white);
				hand_object.set_color(9, Color.white);
			}

			if (hand_object.spheres[16].transform.position.y < hand_object.spheres[15].transform.position.y)
			{
				hand_object.set_color(16, Color.blue);
				hand_object.set_color(15, Color.blue);
				hand_object.set_color(14, Color.blue);
				hand_object.set_color(13, Color.blue);
			}
			else
			{
				hand_object.set_color(16, Color.white);
				hand_object.set_color(15, Color.white);
				hand_object.set_color(14, Color.white);
				hand_object.set_color(13, Color.white);
			}

			if (hand_object.spheres[20].transform.position.y < hand_object.spheres[19].transform.position.y)
			{
				hand_object.set_color(20, Color.blue);
				hand_object.set_color(19, Color.blue);
				hand_object.set_color(18, Color.blue);
				hand_object.set_color(17, Color.blue);
			}
			else
			{
				hand_object.set_color(20, Color.white);
				hand_object.set_color(19, Color.white);
				hand_object.set_color(18, Color.white);
				hand_object.set_color(17, Color.white);
			}
			if (hand_object.spheres[12].transform.position.y < hand_object.spheres[11].transform.position.y)
			{
				if (hand_object.spheres[16].transform.position.y < hand_object.spheres[15].transform.position.y)
				{
					if (hand_object.spheres[8].transform.position.y > hand_object.spheres[7].transform.position.y)
					{
						if (hand_object.spheres[20].transform.position.y > hand_object.spheres[19].transform.position.y)
						{
							for (int i = 5; i < 21; i++)
							{
								hand_object.set_color(i, Color.red);
							}
						}
					}
				}
			}
		}

		if (Input.GetKeyDown(KeyCode.Space))
		{
			//SendMessage();
		}
	}

	/// <summary> 	
	/// Runs in background TcpServerThread; Handles incomming TcpClient requests 	
	/// </summary> 	
	private void ListenForIncommingRequests()
	{
		try
		{
			// Create listener on localhost port 8052. 			
			tcpListener = new TcpListener(IPAddress.Parse(IPManager.GetIP(ADDRESSFAM.IPv4)), 5052);
			tcpListener.Start();
			Debug.Log("Server is listening");
			Byte[] bytes = new Byte[1024];
			while (true)
			{
				using (connectedTcpClient = tcpListener.AcceptTcpClient())
				{
					// Get a stream object for reading 					
					using (NetworkStream stream = connectedTcpClient.GetStream())
					{
						int length;
						// Read incomming stream into byte arrary. 						
						while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
						{
							var incommingData = new byte[length];
							Array.Copy(bytes, 0, incommingData, 0, length);
							// Convert byte array to string message. 							
							string clientMessage = Encoding.ASCII.GetString(incommingData);
							Debug.Log("client message received as: " + clientMessage);
							clientMessage = clientMessage.Replace("[", "");
							clientMessage = clientMessage.Replace("]", "");
							splitArray = clientMessage.Split(char.Parse(","));
							//int number = int.Parse(splitArray[0]);
							int numberttt;
							if (int.TryParse(splitArray[0], out numberttt))
							{
								isTHere = true;
							}
							
						}
					}
				}
			}
		}
		catch (SocketException socketException)
		{
			Debug.Log("SocketException " + socketException.ToString());
		}
	}
	/// <summary> 	
	/// Send message to client using socket connection. 	
	/// </summary> 	
	private void SendMessage()
	{
		if (connectedTcpClient == null)
		{
			return;
		}

		try
		{
			// Get a stream object for writing. 			
			NetworkStream stream = connectedTcpClient.GetStream();
			if (stream.CanWrite)
			{
				string serverMessage = "This is a message from your server.";
				// Convert string message to byte array.                 
				byte[] serverMessageAsByteArray = Encoding.ASCII.GetBytes(serverMessage);
				// Write byte array to socketConnection stream.               
				stream.Write(serverMessageAsByteArray, 0, serverMessageAsByteArray.Length);
				Debug.Log("Server sent his message - should be received by client");
			}
		}
		catch (SocketException socketException)
		{
			Debug.Log("Socket exception: " + socketException);
		}
	}

	public class IPManager
	{
		public static string GetIP(ADDRESSFAM Addfam)
		{
			//Return null if ADDRESSFAM is Ipv6 but Os does not support it
			if (Addfam == ADDRESSFAM.IPv6 && !Socket.OSSupportsIPv6)
			{
				return null;
			}

			string output = "0.0.0.0";

			foreach (NetworkInterface item in NetworkInterface.GetAllNetworkInterfaces())
			{
#if UNITY_EDITOR_WIN || UNITY_STANDALONE_WIN
				NetworkInterfaceType _type1 = NetworkInterfaceType.Wireless80211;
				NetworkInterfaceType _type2 = NetworkInterfaceType.Ethernet;

				if ((item.NetworkInterfaceType == _type1 || item.NetworkInterfaceType == _type2) && item.OperationalStatus == OperationalStatus.Up)
#endif
				{
					foreach (UnicastIPAddressInformation ip in item.GetIPProperties().UnicastAddresses)
					{
						//IPv4
						if (Addfam == ADDRESSFAM.IPv4)
						{
							if (ip.Address.AddressFamily == AddressFamily.InterNetwork)
							{
								if (ip.Address.ToString() != "127.0.0.1")
									output = ip.Address.ToString();
							}
						}

						//IPv6
						else if (Addfam == ADDRESSFAM.IPv6)
						{
							if (ip.Address.AddressFamily == AddressFamily.InterNetworkV6)
							{
								if (ip.Address.ToString() != "127.0.0.1")
									output = ip.Address.ToString();
							}
						}
					}
				}
			}
			return output;
		}
	}

	public enum ADDRESSFAM
	{
		IPv4, IPv6
	}
}